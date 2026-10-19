"""Download everything the model needs into data/ (run from the repository root).

- Bike Share ridership for 2025 and 2026 (City of Toronto Open Data Portal)
- Hourly weather at the Toronto City station (Environment and Climate Change Canada)
- Station list with dock counts (Bike Share Toronto's public GBFS feed)
"""
import io
import os
import urllib.request
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
os.chdir(ROOT)

RIDES = ("https://opendata.toronto.ca/toronto.parking.authority/"
         "bike-share-toronto-ridership-data/bikeshare-ridership-{year}.zip")
WEATHER = ("https://climate.weather.gc.ca/climate_data/bulk_data_e.html?format=csv"
           "&stationID=31688&Year={year}&Month={month}&Day=14&timeframe=1&submit=Download+Data")
GBFS = "https://tor.publicbikesystem.net/ube/gbfs/v1/en/station_information"


def fetch(url):
    with urllib.request.urlopen(url, timeout=600) as r:
        return r.read()


# Ridership: 2025 comes as monthly files (into data/2025/), 2026 as one file (into data/)
for year, folder in [(2025, "data/2025"), (2026, "data")]:
    Path(folder).mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(io.BytesIO(fetch(RIDES.format(year=year)))) as z:
        for name in z.namelist():
            if name.endswith(".csv"):
                Path(folder, Path(name).name).write_bytes(z.read(name))
    print(f"ridership {year}: done")

# Weather, January 2025 - September 2026, one file per month
Path("data/weather").mkdir(parents=True, exist_ok=True)
months = [(2025, m) for m in range(1, 13)] + [(2026, m) for m in range(1, 10)]
for year, month in months:
    Path(f"data/weather/toronto_city_{year}_{month:02d}.csv").write_bytes(
        fetch(WEATHER.format(year=year, month=month)))
print("weather: done")

# Station list with capacities (a snapshot of the current network)
Path("data/station_information.json").write_bytes(fetch(GBFS))
print("station list: done")
