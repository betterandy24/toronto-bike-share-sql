"""Build the modelling tables from the raw files (run from the repository root, after
model/get_data.py). Writes four small files to model/data/, which are kept in the
repository so the models can be re-run without the 2 GB of raw trip data:

  system_hourly.csv.gz    trips started in each hour, January 2025 - September 2026
  station_morning.csv.gz  bikes out / in per station, 7-10 a.m., every working weekday
  weather_hourly.csv.gz   temperature, rain and humidity per hour (local clock time)
  stations.csv            each station's location and number of docks
"""
import glob
import json
import os
from pathlib import Path

import duckdb
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
os.chdir(ROOT)
OUT = ROOT / "model" / "data"
OUT.mkdir(parents=True, exist_ok=True)

COLS = ["Trip_Duration", "Start_Station_Id", "Start_Time", "End_Station_Id", "User_Type"]
raw_2025 = pd.concat(
    (pd.read_csv(f, usecols=COLS, dtype=str, encoding="cp1252")
     for f in sorted(glob.glob("data/2025/*.csv"))),
    ignore_index=True,
)
raw_2025.columns = [c.lower() for c in raw_2025.columns]

con = duckdb.connect(str(ROOT / "model.duckdb"))   # on disk, so DuckDB can spill to disk
con.register("raw_2025_df", raw_2025)
con.execute("CREATE OR REPLACE TABLE raw_2025 AS SELECT * FROM raw_2025_df")
del raw_2025

check = con.execute((ROOT / "model" / "panels.sql").read_text()).df()
print(check.to_string(index=False))

for table in ["system_hourly", "station_morning"]:
    con.execute(f"COPY {table} TO 'model/data/{table}.csv.gz' (HEADER, COMPRESSION gzip)")
con.close()
os.remove(ROOT / "model.duckdb")

# Weather: Environment Canada reports hours in standard time all year, so shift summer
# hours by one to match the trip records, which use local clock time
w = pd.concat((pd.read_csv(f) for f in sorted(glob.glob("data/weather/*.csv"))), ignore_index=True)
w = w.rename(columns={"Date/Time (LST)": "lst", "Temp (°C)": "temp_c",
                      "Precip. Amount (mm)": "precip_mm", "Rel Hum (%)": "humidity"})
utc = pd.to_datetime(w["lst"]) + pd.Timedelta(hours=5)
w["hour_start"] = utc.dt.tz_localize("UTC").dt.tz_convert("America/Toronto").dt.tz_localize(None)
w = (w[["hour_start", "temp_c", "precip_mm", "humidity"]]
     .drop_duplicates("hour_start").set_index("hour_start").sort_index()
     .interpolate(limit=6).reset_index())
w.to_csv(OUT / "weather_hourly.csv.gz", index=False)

# Stations: location and dock count from the GBFS snapshot
info = json.loads(Path("data/station_information.json").read_text())
st = pd.DataFrame(info["data"]["stations"])[["station_id", "name", "lat", "lon", "capacity"]]
st["station_id"] = st["station_id"].astype(int)
st["name"] = st["name"].str.split().str.join(" ")
st.to_csv(OUT / "stations.csv", index=False)
print(f"Wrote model/data/ (station list as of {pd.to_datetime(info['last_updated'], unit='s'):%Y-%m-%d})")
