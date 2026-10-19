"""Run every SQL file in sql/ against the trip data in data/ and save the results.

Usage (from this folder):  python run_all.py
Outputs: results/*.csv, results/summary.md and figures/*.png
"""
import os
from pathlib import Path

import duckdb
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parent
os.chdir(ROOT)                      # so 'data/*.csv' in the SQL resolves correctly
(ROOT / "results").mkdir(exist_ok=True)
(ROOT / "figures").mkdir(exist_ok=True)

# A database file on disk (not in memory) lets DuckDB spill to disk, so a ~1 GB CSV
# runs on an ordinary laptop. The file is rebuilt each run and is not committed.
con = duckdb.connect("bikeshare.duckdb")
summary = ["# Query results\n"]

for path in sorted((ROOT / "sql").glob("*.sql")):
    sql = path.read_text(encoding="utf-8")
    df = con.execute(sql).df()      # runs every statement; returns the last SELECT
    df.to_csv(ROOT / "results" / f"{path.stem}.csv", index=False)
    title = sql.splitlines()[0].lstrip("- ").strip()
    summary += [f"## {title}\n", "```", df.to_string(index=False), "```\n"]
    print(f"{path.name}: {len(df)} rows")
    if path.stem.startswith("01"):
        print(df.to_string(index=False))
        # Sanity check: every label should map to Member/Casual and Classic/E-bike
        print(con.execute("""SELECT user_type, bike_model, rider_type, bike_type, COUNT(*) AS n
                             FROM parsed_trips JOIN trips USING (trip_id)
                             GROUP BY ALL ORDER BY n DESC""").df().to_string(index=False))

(ROOT / "results" / "summary.md").write_text("\n".join(summary), encoding="utf-8")

# ---- Charts ----
monthly = con.execute("SELECT * FROM read_csv('results/02_monthly.csv')").df()
fig, ax = plt.subplots(figsize=(9, 4))
ax.bar(monthly["month"], monthly["member_trips"] / 1000, label="Members")
ax.bar(monthly["month"], monthly["casual_trips"] / 1000,
       bottom=monthly["member_trips"] / 1000, label="Casual riders")
ax.set_ylabel("Trips (thousands)")
ax.set_title("Bike Share Toronto trips per month")
ax.tick_params(axis="x", rotation=45)
ax.legend()
fig.tight_layout()
fig.savefig("figures/monthly_trips.png", dpi=150)

hourly = con.execute("SELECT * FROM read_csv('results/03_hourly.csv')").df()
# One panel per day type, one line per rider type, so both comparisons are visible
fig, axes = plt.subplots(1, 2, figsize=(11, 4), sharey=True)
for ax, day_type in zip(axes, ["Weekday", "Weekend/holiday"]):
    d = hourly[hourly["day_type"] == day_type]
    for rider, color in [("Member", "#1f77b4"), ("Casual", "#ff7f0e")]:
        r = d[d["rider_type"] == rider]
        ax.plot(r["hour"], r["avg_trips_per_day"], color=color, linewidth=2, label=rider)
        ax.annotate(rider, (r["hour"].iloc[-1], r["avg_trips_per_day"].iloc[-1]),
                    xytext=(4, 0), textcoords="offset points", va="center", fontsize=9)
    ax.set_title("Weekdays" if day_type == "Weekday" else "Weekends and public holidays")
    ax.set_xticks(range(0, 24, 3))
    ax.set_xlim(0, 26)
    ax.set_xlabel("Hour of day (trip start)")
    ax.grid(axis="y", alpha=0.3)
    for side in ["top", "right"]:
        ax.spines[side].set_visible(False)
axes[0].set_ylabel("Average trips per day")
axes[0].set_ylim(bottom=0)
handles, labels = axes[0].get_legend_handles_labels()
fig.legend(handles, labels, loc="upper right", ncol=2, frameon=False)
fig.suptitle("Members ride to work; casual riders ride in the afternoon and at weekends",
             x=0.02, ha="left")
fig.tight_layout(rect=(0, 0, 1, 0.95))
fig.savefig("figures/hourly_pattern.png", dpi=150)

imb = con.execute("SELECT * FROM read_csv('results/06_imbalance.csv')").df()
fig, ax = plt.subplots(figsize=(9, 6))
colors = ["#c0392b" if v < 0 else "#2471a3" for v in imb["net_bikes_per_morning"]]
ax.barh(imb["station_name"], imb["net_bikes_per_morning"], color=colors)
ax.axvline(0, color="black", linewidth=0.8)
ax.invert_yaxis()
ax.set_xlabel("Bikes returned minus bikes taken, per weekday morning (7-10 a.m., May-Sept)")
ax.set_title("Stations that empty out (red) or fill up (blue) in the morning rush")
fig.tight_layout()
fig.savefig("figures/morning_imbalance.png", dpi=150)

print("Done: results/summary.md and figures/*.png")
