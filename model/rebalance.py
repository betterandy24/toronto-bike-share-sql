"""Part 2b - Plan the morning rebalancing and test the plans (run after forecast.py).

Question: before 7 a.m., the operator's trucks can move a limited number of bikes. Which
stations should they take bikes from, and which should they fill, so that as few riders
as possible meet an empty station (no bike) or a full one (no free dock) by 10 a.m.?

Step 1 (integer programme, PuLP + HiGHS): given each station's dock count and its forecast
net flow for 7-10 a.m., choose how many bikes each station should hold at 7 a.m.
Step 2 (transport problem): pair the stations losing bikes with the stations gaining them
so as to minimise the total straight-line distance (station pairs, not truck routes).

The plans are then replayed against what riders actually did on each working weekday of
July-September 2026. Assumptions, stated plainly:
- Every station starts the morning half full. The data does not record how many bikes
  were really at each station, so the comparison is between plans, not with reality.
- Only the morning's net flow is used (bikes in minus bikes out). Within-morning timing
  can make things worse than this, so the counts below are a lower bound.
- Dock counts come from the current station list (October 2026).
"""
import os
from pathlib import Path

import matplotlib
import numpy as np
import pandas as pd
import pulp

matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parent.parent
os.chdir(ROOT)
D, RES = Path("model/data"), Path("model/results")

BUDGETS = [100, 250, 500, 1000]        # bikes the trucks can move before 7 a.m.
MAIN_BUDGET = 500
EXAMPLE_DAY = pd.Timestamp("2026-07-15")
MOVE_COST = 0.001                      # tiny cost per bike moved, so no needless moves
MARGIN, MARGIN_WEIGHT = 3, 0.2         # try to keep 3 bikes / 3 docks spare as a safety buffer


def plan_inventory(cap, start, net_forecast, budget, margin=MARGIN):
    """Bikes to hold at each station at 7 a.m. (step 1)."""
    n = len(cap)
    prob = pulp.LpProblem("morning_rebalancing", pulp.LpMinimize)
    add = [pulp.LpVariable(f"add_{i}", 0, cat="Integer") for i in range(n)]
    remove = [pulp.LpVariable(f"remove_{i}", 0, cat="Integer") for i in range(n)]
    empty = [pulp.LpVariable(f"empty_{i}", 0) for i in range(n)]    # riders finding no bike
    full = [pulp.LpVariable(f"full_{i}", 0) for i in range(n)]      # riders finding no dock
    # Forecasts are uncertain, so a smaller penalty applies when the forecast ending stock
    # comes within MARGIN of empty or full; this also makes the planner take bikes from
    # stations with the most to spare rather than from any station that just about copes
    thin_e = [pulp.LpVariable(f"thin_e_{i}", 0) for i in range(n)]
    thin_f = [pulp.LpVariable(f"thin_f_{i}", 0) for i in range(n)]
    prob += (pulp.lpSum(empty) + pulp.lpSum(full)
             + MARGIN_WEIGHT * (pulp.lpSum(thin_e) + pulp.lpSum(thin_f))
             + MOVE_COST * pulp.lpSum(add + remove))
    prob += pulp.lpSum(add) == pulp.lpSum(remove)            # bikes are moved, not created
    prob += pulp.lpSum(add) <= budget                        # truck capacity this morning
    for i in range(n):
        held = start[i] + add[i] - remove[i]
        prob += held >= 0
        prob += held <= cap[i]
        prob += empty[i] >= -(held + net_forecast[i])        # stock runs below zero
        prob += full[i] >= held + net_forecast[i] - cap[i]   # stock runs above dock count
        prob += thin_e[i] >= margin - (held + net_forecast[i])
        prob += thin_f[i] >= held + net_forecast[i] - (cap[i] - margin)
    prob.solve(pulp.HiGHS(msg=False))
    assert pulp.LpStatus[prob.status] == "Optimal"
    return np.array([start[i] + add[i].value() - remove[i].value() for i in range(n)])


def replay(cap, held, net_actual):
    """Riders who would meet an empty or a full station, given the actual net flow."""
    end = held + net_actual
    return np.maximum(0, -end).sum(), np.maximum(0, end - cap).sum()


def truck_moves(stations, held, start):
    """Pair stations giving bikes with stations receiving them, minimising total straight-line
    km (step 2). This pairs stations; it does not plan the trucks' actual routes."""
    change = held - start
    give = stations[change < -0.5].assign(bikes=-change[change < -0.5])
    take = stations[change > 0.5].assign(bikes=change[change > 0.5])
    lat0 = np.radians(43.65)
    def km(a, b):
        dx = (a.lon - b.lon) * 111.32 * np.cos(lat0)
        dy = (a.lat - b.lat) * 110.57
        return float(np.hypot(dx, dy))
    prob = pulp.LpProblem("truck_moves", pulp.LpMinimize)
    x = {(i, j): pulp.LpVariable(f"x_{i}_{j}", 0) for i in give.index for j in take.index}
    prob += pulp.lpSum(km(give.loc[i], take.loc[j]) * v for (i, j), v in x.items())
    for i in give.index:
        prob += pulp.lpSum(x[i, j] for j in take.index) == give.loc[i, "bikes"]
    for j in take.index:
        prob += pulp.lpSum(x[i, j] for i in give.index) == take.loc[j, "bikes"]
    prob.solve(pulp.HiGHS(msg=False))
    moves = [(give.loc[i, "name"], take.loc[j, "name"], v.value(), km(give.loc[i], take.loc[j]))
             for (i, j), v in x.items() if v.value() and v.value() > 0.5]
    return pd.DataFrame(moves, columns=["from_station", "to_station", "bikes", "km"])


fc = pd.read_csv(D / "station_morning_forecasts.csv.gz", parse_dates=["date"])
st = pd.read_csv(D / "stations.csv")
fc = fc.merge(st, on="station_id", how="left")
covered = fc["capacity"].notna()
share = (fc.loc[covered, "bikes_out"].sum() + fc.loc[covered, "bikes_in"].sum()) / \
        (fc["bikes_out"].sum() + fc["bikes_in"].sum())
print(f"Stations with a known dock count carry {100 * share:.1f}% of test-period morning trips")
fc = fc[covered & (fc["capacity"] > 0)].copy()
fc["net"] = fc["bikes_in"] - fc["bikes_out"]
for m in ["avg4w", "lightgbm"]:
    fc[f"net_{m}"] = fc[f"bikes_in_pred_{m}"] - fc[f"bikes_out_pred_{m}"]
fc["net_perfect"] = fc["net"]

rows, example = [], {}
for day, d in fc.groupby("date"):
    d = d.reset_index(drop=True)
    cap = d["capacity"].to_numpy(float)
    start = np.floor(cap / 2)
    net = d["net"].to_numpy(float)
    e, f = replay(cap, start, net)
    rows.append(dict(date=day, plan="No rebalancing", budget=0, no_bike=e, no_dock=f))
    for budget in BUDGETS:
        for m, label in [("avg4w", "Plan from 4-week average"),
                         ("lightgbm", "Plan from LightGBM forecast"),
                         ("perfect", "Plan with perfect foresight")]:
            held = plan_inventory(cap, start, d[f"net_{m}"].to_numpy(float), budget)
            e, f = replay(cap, held, net)
            rows.append(dict(date=day, plan=label, budget=budget, no_bike=e, no_dock=f))
            if day == EXAMPLE_DAY and budget == MAIN_BUDGET and m == "lightgbm":
                example = dict(d=d, held=held, start=start)

            if budget == MAIN_BUDGET and m != "perfect":
                for margin in [0, 6]:                # how much does the safety buffer matter?
                    held_m = plan_inventory(cap, start, d[f"net_{m}"].to_numpy(float), budget, margin)
                    e, f = replay(cap, held_m, net)
                    rows.append(dict(date=day, plan=f"{label} (buffer {margin})", budget=budget,
                                     no_bike=e, no_dock=f))

sim = pd.DataFrame(rows)
sim["failed"] = sim["no_bike"] + sim["no_dock"]
summary = (sim.groupby(["plan", "budget"])[["no_bike", "no_dock", "failed"]].mean()
           .round(0).reset_index())
summary.to_csv(RES / "rebalancing_summary.csv", index=False)
print(summary.to_string(index=False))

# Problems no morning plan can fix: stations whose net flow is bigger than their dock count
d_all = fc.assign(beyond=np.maximum(0, fc["net"].abs() - fc["capacity"]))
beyond_per_day = d_all.groupby("date")["beyond"].sum().mean()
worst = (d_all.groupby("name")
         .agg(capacity=("capacity", "first"), avg_net=("net", "mean"), beyond=("beyond", "mean"))
         .sort_values("beyond", ascending=False).head(8).round(1))
worst.to_csv(RES / "beyond_capacity_stations.csv")
print(f"Flow beyond dock capacity, per morning: {beyond_per_day:.0f}")
print(worst.to_string())

# Truck moves on the example day
moves = truck_moves(example["d"], example["held"], example["start"])
moves = moves.sort_values("bikes", ascending=False).round(1)
moves.to_csv(RES / "example_day_moves.csv", index=False)
print(f"{EXAMPLE_DAY:%d %b %Y}: {moves['bikes'].sum():.0f} bikes in {len(moves)} moves, "
      f"{(moves['bikes'] * moves['km']).sum() / moves['bikes'].sum():.1f} straight-line km per bike on average")
print(moves.head(10).to_string(index=False))

# Chart: riders meeting an empty or full station, by plan and truck budget
fig, ax = plt.subplots(figsize=(9, 4.5))
base = summary.query("plan == 'No rebalancing'")["failed"].iloc[0]
ax.axhline(base, color="#999999", linestyle="--", linewidth=1.2)
ax.text(BUDGETS[-1], base, " No rebalancing", va="bottom", ha="right", fontsize=9, color="#555555")
styles = {"Plan from 4-week average": ("#ff7f0e", "s"),
          "Plan from LightGBM forecast": ("#1f77b4", "o"),
          "Plan with perfect foresight": ("#2ca02c", "^")}
for plan, (color, marker) in styles.items():
    p = summary[summary["plan"] == plan]
    ax.plot(p["budget"], p["failed"], color=color, marker=marker, linewidth=2, label=plan)
ax.axhline(beyond_per_day, color="#c0392b", linestyle=":", linewidth=1.2)
ax.text(BUDGETS[0], beyond_per_day, "Out of reach of any morning plan (flow larger than the docks)",
        va="top", fontsize=8.5, color="#c0392b")
ax.set_xscale("log")
ax.minorticks_off()
ax.set_xticks(BUDGETS)
ax.set_xticklabels([str(b) for b in BUDGETS])
ax.set_ylim(bottom=0)
ax.set_xlabel("Bikes the trucks move before 7 a.m.")
ax.set_ylabel("Riders meeting an empty or full station\n(per weekday morning, 7-10 a.m.)")
ax.set_title("Simulated July-September 2026 weekday mornings")
ax.legend(frameon=False, fontsize=9, loc="lower left")
for side in ["top", "right"]:
    ax.spines[side].set_visible(False)
fig.tight_layout()
fig.savefig("figures/rebalancing_simulation.png", dpi=150)
