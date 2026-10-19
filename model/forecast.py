"""Part 2a - Forecast demand (run from the repository root, after build_panels.py).

Two forecasts, both made one day ahead and tested on July-September 2026, a period the
models never see while being fitted (training data: January 2025 - June 2026):

1. Citywide trips per hour. Compares a naive rule (same hour last week), a regression
   and a gradient-boosted tree model (LightGBM).
2. Bikes taken out and returned at each station between 7 and 10 a.m. on working
   weekdays, the numbers a rebalancing plan needs. Compares two rules of thumb with
   LightGBM.

Weather enters as observed values, standing in for a next-day weather forecast; real
forecasts are less accurate, so these errors are a best case for the weather part.
"""
import os
from pathlib import Path

import lightgbm as lgb
import matplotlib
import numpy as np
import pandas as pd
import statsmodels.formula.api as smf

matplotlib.use("Agg")
import matplotlib.dates
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parent.parent
os.chdir(ROOT)
D = Path("model/data")
RES = Path("model/results")
RES.mkdir(exist_ok=True)
TEST_START, TEST_END = pd.Timestamp("2026-07-01"), pd.Timestamp("2026-10-01")
VALID_START = pd.Timestamp("2026-05-01")      # last part of training, for early stopping
SEED = 0


def wape(y, yhat):
    """Total absolute error as a share of total trips (lower is better)."""
    return np.abs(y - yhat).sum() / y.sum()


def fit_lgbm(train, features, target, cat=()):
    """Poisson LightGBM: pick the number of trees on the last two months of training,
    then refit on all of training with that number."""
    params = dict(objective="poisson", learning_rate=0.03, num_leaves=63,
                  min_data_in_leaf=50, feature_fraction=0.8, bagging_fraction=0.8,
                  bagging_freq=1, seed=SEED, verbose=-1)
    early = train[train["date"] < VALID_START]
    valid = train[train["date"] >= VALID_START]
    d_tr = lgb.Dataset(early[features], early[target], categorical_feature=list(cat))
    d_va = lgb.Dataset(valid[features], valid[target], categorical_feature=list(cat))
    probe = lgb.train(params, d_tr, 3000, valid_sets=[d_va],
                      callbacks=[lgb.early_stopping(100, verbose=False)])
    d_all = lgb.Dataset(train[features], train[target], categorical_feature=list(cat))
    return lgb.train(params, d_all, probe.best_iteration)


# =========================================================================================
# 1. Citywide trips per hour
# =========================================================================================
h = pd.read_csv(D / "system_hourly.csv.gz", parse_dates=["hour_start"])
w = pd.read_csv(D / "weather_hourly.csv.gz", parse_dates=["hour_start"])
h = h.merge(w, on="hour_start", how="left").sort_values("hour_start")
h[["temp_c", "precip_mm", "humidity"]] = h[["temp_c", "precip_mm", "humidity"]].ffill()

t = h["hour_start"]
h["date"] = t.dt.normalize()
h["hour"] = t.dt.hour
h["dow"] = t.dt.dayofweek
h["month"] = t.dt.month
h["doy"] = t.dt.dayofyear
h["day_off"] = ((h["dow"] >= 5) | h["is_holiday"]).astype(int)
h["rain"] = (h["precip_mm"] > 0).astype(int)
h["rain_prev3h"] = h["precip_mm"].rolling(3, min_periods=1).sum().shift(1).fillna(0)
# Known one day ahead: the same hour yesterday and last week, and the average hour over
# the last seven full days (a running measure of the current level of demand)
h["lag_24"] = h["trips"].shift(24)
h["lag_168"] = h["trips"].shift(168)
daily = h.groupby("date")["trips"].sum()
level = (daily.rolling(7).mean().shift(1) / 24).rename("level_7d")
h = h.merge(level, left_on="date", right_index=True, how="left")
h = h.dropna(subset=["lag_168", "level_7d"]).reset_index(drop=True)

train = h[h["date"] < TEST_START]
test = h[(h["date"] >= TEST_START) & (h["date"] < TEST_END)].copy()

# (a) Naive rule: same hour last week
test["pred_naive"] = test["lag_168"]

# (b) Regression on log trips: hour-of-day profile for working days and days off, month,
#     weather and recent demand
formula = ("np.log1p(trips) ~ C(hour):C(day_off) + C(month) + temp_c + I(temp_c**2)"
           " + rain + np.log1p(rain_prev3h) + humidity"
           " + np.log1p(lag_24) + np.log1p(lag_168) + np.log1p(level_7d)")
ols = smf.ols(formula, data=train).fit()
smear = np.mean(np.exp(ols.resid))          # converts a log forecast back to trips
test["pred_regression"] = np.expm1(ols.predict(test)) * smear

# (c) LightGBM with the same information
H_FEATURES = ["hour", "dow", "day_off", "month", "doy", "temp_c", "precip_mm", "rain_prev3h",
              "humidity", "lag_24", "lag_168", "level_7d"]
gbm_h = fit_lgbm(train, H_FEATURES, "trips")
test["pred_lightgbm"] = gbm_h.predict(test[H_FEATURES])

rows = []
for name in ["naive", "regression", "lightgbm"]:
    p = test[f"pred_{name}"]
    day = test.groupby("date")[["trips", f"pred_{name}"]].sum()
    rows.append({"model": name,
                 "mae_trips_per_hour": round(np.abs(test["trips"] - p).mean(), 1),
                 "wape_hourly_pct": round(100 * wape(test["trips"], p), 1),
                 "wape_daily_total_pct": round(100 * wape(day["trips"], day[f"pred_{name}"]), 1)})
hourly_scores = pd.DataFrame(rows)
hourly_scores.to_csv(RES / "forecast_hourly_scores.csv", index=False)
print(hourly_scores.to_string(index=False))

# What the regression says about weather (holding time of day, season and recent demand fixed)
b = ols.params
b2 = b[[k for k in b.index if k.startswith("I(temp_c")][0]]
weather_effects = pd.DataFrame({
    "effect": ["Rain falling in that hour",
               "1 mm of rain in the previous 3 hours (vs none)",
               "10 C warmer (from 10 C to 20 C)"],
    "change_in_trips_pct": [
        100 * (np.exp(b["rain"]) - 1),
        100 * (np.exp(b["np.log1p(rain_prev3h)"] * np.log(2)) - 1),
        100 * (np.exp(b["temp_c"] * 10 + b2 * (400 - 100)) - 1)],
}).round(1)
weather_effects.to_csv(RES / "weather_effects.csv", index=False)
print(weather_effects.to_string(index=False))

# Chart: one test week, actual vs forecasts
wk = test[(test["date"] >= "2026-07-13") & (test["date"] < "2026-07-20")]
fig, ax = plt.subplots(figsize=(11, 4))
ax.plot(wk["hour_start"], wk["trips"], color="black", linewidth=2, label="Actual")
ax.plot(wk["hour_start"], wk["pred_naive"], color="#999999", linewidth=1.2,
        linestyle="--", label="Same hour last week")
ax.plot(wk["hour_start"], wk["pred_lightgbm"], color="#1f77b4", linewidth=1.5,
        label="LightGBM forecast")
rainy = wk[wk["precip_mm"] > 0.5]
ax.scatter(rainy["hour_start"], np.zeros(len(rainy)) - 120, marker="|", s=80,
           color="#2ca02c", label="Rain (> 0.5 mm in the hour)")
ax.set_ylabel("Trips started per hour")
ax.set_title("Citywide demand, 13-19 July 2026 (test period): forecast vs actual")
ax.legend(frameon=False, ncol=4, loc="upper center", bbox_to_anchor=(0.5, -0.12), fontsize=9)
ax.xaxis.set_major_formatter(matplotlib.dates.DateFormatter("%a %d %b"))
for side in ["top", "right"]:
    ax.spines[side].set_visible(False)
fig.tight_layout()
fig.savefig("figures/forecast_hourly_week.png", dpi=150)

# =========================================================================================
# 2. Station mornings: bikes out and in, 7-10 a.m., working weekdays
# =========================================================================================
s = pd.read_csv(D / "station_morning.csv.gz", parse_dates=["ride_date"])
s = s.rename(columns={"ride_date": "date"}).sort_values(["station_id", "date"])
morning_w = (w.assign(date=w["hour_start"].dt.normalize(), hour=w["hour_start"].dt.hour)
             .query("7 <= hour <= 9")
             .groupby("date").agg(temp_am=("temp_c", "mean"), rain_am=("precip_mm", "sum"))
             .reset_index())
s = s.merge(morning_w, on="date", how="left")
s["dow"] = s["date"].dt.dayofweek
s["month"] = s["date"].dt.month

# Same weekday last week (by calendar date, so weeks with a holiday don't shift the match)
last_week = s[["station_id", "date", "bikes_out", "bikes_in"]].copy()
last_week["date"] = last_week["date"] + pd.Timedelta(days=7)
s = s.merge(last_week, on=["station_id", "date"], how="left", suffixes=("", "_lag1w"))
g = s.groupby("station_id")
for col in ["bikes_out", "bikes_in"]:
    s[f"{col}_lag1w"] = s[f"{col}_lag1w"].fillna(g[col].shift(5))      # holiday last week
    s[f"{col}_avg4w"] = g[col].transform(lambda x: x.shift(1).rolling(20, min_periods=10).mean())
    s[f"{col}_lag1d"] = g[col].shift(1)                                   # previous working day
s = s.dropna(subset=["bikes_out_avg4w", "bikes_out_lag1w"]).reset_index(drop=True)
s["station"] = s["station_id"].astype("category")

S_FEATURES = ["station", "dow", "month", "temp_am", "rain_am",
              "bikes_out_lag1w", "bikes_out_avg4w", "bikes_out_lag1d",
              "bikes_in_lag1w", "bikes_in_avg4w", "bikes_in_lag1d"]
strain = s[s["date"] < TEST_START]
stest = s[(s["date"] >= TEST_START) & (s["date"] < TEST_END)].copy()

for col in ["bikes_out", "bikes_in"]:
    stest[f"{col}_pred_lastweek"] = stest[f"{col}_lag1w"]
    stest[f"{col}_pred_avg4w"] = stest[f"{col}_avg4w"]
    model = fit_lgbm(strain, S_FEATURES, col, cat=["station"])
    stest[f"{col}_pred_lightgbm"] = model.predict(stest[S_FEATURES])

stest["net"] = stest["bikes_in"] - stest["bikes_out"]
rows = []
for name in ["lastweek", "avg4w", "lightgbm"]:
    net_pred = stest[f"bikes_in_pred_{name}"] - stest[f"bikes_out_pred_{name}"]
    rows.append({
        "model": {"lastweek": "Same weekday last week", "avg4w": "Average of last 4 weeks",
                  "lightgbm": "LightGBM"}[name],
        "mae_bikes_out": round(np.abs(stest["bikes_out"] - stest[f"bikes_out_pred_{name}"]).mean(), 2),
        "mae_bikes_in": round(np.abs(stest["bikes_in"] - stest[f"bikes_in_pred_{name}"]).mean(), 2),
        "mae_net": round(np.abs(stest["net"] - net_pred).mean(), 2),
        "wape_net_pct": round(100 * np.abs(stest["net"] - net_pred).sum() / np.abs(stest["net"]).sum(), 1),
    })
station_scores = pd.DataFrame(rows)
station_scores.to_csv(RES / "forecast_station_scores.csv", index=False)
print(station_scores.to_string(index=False))

keep = ["date", "station_id", "bikes_out", "bikes_in"] + [
    f"{c}_pred_{m}" for c in ["bikes_out", "bikes_in"] for m in ["lastweek", "avg4w", "lightgbm"]]
stest[keep].to_csv(D / "station_morning_forecasts.csv.gz", index=False, float_format="%.2f")
print(f"test: {test['date'].nunique()} days, {stest['date'].nunique()} working weekdays, "
      f"{stest['station_id'].nunique()} stations")
