# Toronto Bike Share in SQL: 6.8 million trips, January–September 2026

How do Torontonians use Bike Share, and where does the system come under strain?
This project answers eight business questions with SQL (DuckDB) on every trip recorded
from January to September 2026, and turns the answers into findings an operator could act on.

![Stations that empty out or fill up in the morning rush](figures/morning_imbalance.png)

## Key findings

1. **The morning rush moves bikes into the Financial District, and they don't come back on their own.**
   On a typical weekday morning (7–10 a.m.), the station at King St W / Bay St (West Side)
   receives about 185 bikes but sends out only about 3. That leaves a surplus of roughly
   180 bikes to clear every morning. Six of the ten busiest morning routes end at this one
   station. Residential stations around Fort York, CityPlace and Liberty Village lose bikes at the same time.
   These are the first places a rebalancing crew should go.
2. **Members commute; casual riders explore.** Members make 69% of trips. Their weekday
   riding peaks at 8 a.m. and 5 p.m. Casual riders take longer trips: about 15.5 minutes
   for a typical ride, against 10.6 for members. They are more than four times as likely
   to ride for over 30 minutes (23% vs 5%), and they ride more at weekends.
3. **Demand is highly seasonal.** August had 11 times as many trips as February
   (1.26 million vs 0.11 million). The casual share of riders rose from 8% in winter to 37%
   in August. Winter riders are almost all members.
4. **A small group of stations carries most of the system.** The busiest 10% of the
   1,098 stations account for 39% of all departures. The quietest half account for only 7%.
5. **The single busiest station is a leisure spot, not a commuter hub.** Centre Island
   Ferry Dock tops the list, and 96% of its riders are casual. All ten of the most popular
   routes overall are on the Toronto Islands.

| | Members | Casual riders |
|---|---|---|
| Share of trips | 68.5% | 31.5% |
| Typical (median) trip | 10.6 min | 15.5 min |
| Longest 10% of trips start at | 24 min | 55 min |
| Trips over 30 minutes | 5.0% | 23.0% |
| Trips taken at weekends | 23.5% | 34.5% |
| Trips on e-bikes | 19.5% | 24.8% |

![Weekday vs weekend riding by hour](figures/hourly_pattern.png)

![Trips per month](figures/monthly_trips.png)

## The questions and the SQL behind them

| File | Question | SQL techniques |
|---|---|---|
| `01_clean.sql` | Load and clean the raw trip file | Reading CSV straight from disk, explicit type conversion (`TRY_CAST`, `TRY_STRPTIME`), regex column matching, `CASE` recoding, a data-quality report built with `UNION ALL` and `FILTER` |
| `02_monthly.sql` | How does ridership change through the year? | `GROUP BY` month, conditional counts (`FILTER`), `MEDIAN`, month-over-month change with `LAG` |
| `03_hourly.sql` | When during the day do people ride? | Common table expressions (CTEs), averaging per day, share of the day with `SUM() OVER (PARTITION BY …)` |
| `04_top_stations.sql` | Which stations are busiest? | `RANK`, running totals with window frames, joining to a station lookup table |
| `05_concentration.sql` | How unequal is demand across stations? | `NTILE(10)` to split stations into ten equal groups |
| `06_imbalance.sql` | Which stations empty out or fill up in the morning? | `UNION ALL` to stack departures and arrivals, `CROSS JOIN` to normalise per day, two-way ranking |
| `07_routes.sql` | What are the most popular routes, overall and for commuters? | Two joins to the same table (start and end station), `ROW_NUMBER` within groups |
| `08_riders.sql` | How do members and casual riders differ? | Percentiles (`QUANTILE_CONT`), shares built from `CASE` inside `AVG` |

`run_all.py` runs the eight files in order. It saves each answer to `results/` and draws
the three charts. The full output of every query is in
[`results/summary.md`](results/summary.md).

## Data cleaning

| Step | Trips |
|---|---|
| Records in the file | 6,830,174 |
| Missing a start or end station | 12,951 |
| Shorter than 1 minute or longer than 3 hours | 26,934 |
| **Kept for analysis** | **6,790,289 (99.4%)** |

Very short trips are usually a rider re-docking the same bike. Very long ones are usually
bikes that were not returned properly. Each station gets the name it appears under most
often, and extra spaces in names are removed. Rider labels are mapped to "Member" or
"Casual" in a way that also works for older files, which used "Annual Member" and
"Casual Member". The few trips on an unlisted bike model (ASTRO, 1%) are kept, but they
are not counted as e-bikes.

## Limitations

- The data covers January–September 2026 only, so the winter months are underrepresented.
- Public holidays are counted as weekdays, which slightly lowers the weekday-morning averages.
- Trip records show only where a ride starts and ends. They don't show bikes moved by
  the operator's trucks, so the morning surplus measures *rider* flows, not how full each
  station actually was.

## How to run it

1. Download the 2026 ridership file from the
   [City of Toronto Open Data Portal](https://open.toronto.ca/dataset/bike-share-toronto-ridership-data/)
   and put the CSV in a folder called `data/`. The raw data, about 1 GB, is not included
   in this repository.
2. `pip install -r requirements.txt`
3. `python run_all.py` (takes 1–2 minutes)

## Data source

Bike Share Toronto Ridership Data, City of Toronto Open Data Portal. Contains information
licensed under the
[Open Government Licence – Toronto](https://open.toronto.ca/open-data-license/).
