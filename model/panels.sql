-- Builds the two tables the forecasting and rebalancing models use, from every trip in
-- January 2025 - September 2026. Same cleaning rules as sql/01_clean.sql.
--   system_hourly   : trips started in each hour (zero-filled), for the citywide forecast
--   station_morning : bikes taken out and returned at each station between 7 and 10 a.m.
--                     on each working weekday, for the station forecast and rebalancing

-- 2025 comes as monthly files in a Windows encoding that DuckDB cannot read directly, so
-- build_panels.py loads them first as the table raw_2025; 2026 is one UTF-8 file
CREATE OR REPLACE VIEW raw_all AS
SELECT * FROM raw_2025
UNION ALL BY NAME
SELECT * FROM read_csv('data/*.csv', all_varchar = true, union_by_name = true,
                       normalize_names = true);

CREATE OR REPLACE TABLE trips_all AS
WITH parsed AS (
    SELECT
        TRY_CAST(TRY_CAST(start_station_id AS DOUBLE) AS INTEGER) AS start_station_id,
        TRY_CAST(TRY_CAST(end_station_id AS DOUBLE) AS INTEGER)   AS end_station_id,
        COALESCE(TRY_STRPTIME(start_time, '%Y-%m-%d %H:%M:%S'),
                 TRY_STRPTIME(start_time, '%m/%d/%Y %H:%M'))       AS start_time,
        TRY_CAST(trip_duration AS INTEGER)                        AS duration_s,
        CASE WHEN user_type ILIKE '%casual%' THEN 'Casual' ELSE 'Member' END AS rider_type
    FROM raw_all
)
SELECT *, CAST(start_time AS DATE) AS ride_date, hour(start_time) AS ride_hour
FROM parsed
WHERE start_station_id IS NOT NULL AND end_station_id IS NOT NULL
  AND start_time >= TIMESTAMP '2025-01-01' AND start_time < TIMESTAMP '2026-10-01'
  AND duration_s BETWEEN 60 AND 3 * 3600;

-- Ontario public holidays, plus Toronto's Civic Holiday
CREATE OR REPLACE TABLE holidays AS
SELECT CAST(d AS DATE) AS holiday_date
FROM (VALUES ('2025-01-01'), ('2025-02-17'), ('2025-04-18'), ('2025-05-19'), ('2025-07-01'),
             ('2025-08-04'), ('2025-09-01'), ('2025-10-13'), ('2025-12-25'), ('2025-12-26'),
             ('2026-01-01'), ('2026-02-16'), ('2026-04-03'), ('2026-05-18'), ('2026-07-01'),
             ('2026-08-03'), ('2026-09-07')) AS t(d);

-- Citywide trips per hour; hours with no trips are kept as zeros
CREATE OR REPLACE TABLE system_hourly AS
WITH hours AS (
    SELECT hour_start
    FROM generate_series(TIMESTAMP '2025-01-01 00:00', TIMESTAMP '2026-09-30 23:00',
                         INTERVAL 1 HOUR) AS g(hour_start)
),
counts AS (
    SELECT date_trunc('hour', start_time)                 AS hour_start,
           COUNT(*)                                       AS trips,
           COUNT(*) FILTER (WHERE rider_type = 'Casual')  AS casual_trips
    FROM trips_all
    GROUP BY 1
)
SELECT h.hour_start,
       COALESCE(c.trips, 0)                               AS trips,
       COALESCE(c.casual_trips, 0)                        AS casual_trips,
       (hol.holiday_date IS NOT NULL)                     AS is_holiday
FROM hours h
LEFT JOIN counts c USING (hour_start)
LEFT JOIN holidays hol ON hol.holiday_date = CAST(h.hour_start AS DATE)
ORDER BY h.hour_start;

-- Working weekdays (no weekends, no public holidays)
CREATE OR REPLACE TABLE workdays AS
SELECT CAST(d AS DATE) AS ride_date
FROM generate_series(DATE '2025-01-01', DATE '2026-09-30', INTERVAL 1 DAY) AS g(d)
WHERE dayofweek(d) NOT IN (0, 6)
  AND CAST(d AS DATE) NOT IN (SELECT holiday_date FROM holidays);

-- Each station's first and last day in service (any trip, any time of day)
CREATE OR REPLACE TABLE station_life AS
SELECT station_id, MIN(ride_date) AS first_day, MAX(ride_date) AS last_day
FROM (SELECT start_station_id AS station_id, ride_date FROM trips_all
      UNION ALL
      SELECT end_station_id, ride_date FROM trips_all)
GROUP BY station_id;

-- Bikes out and in between 7 and 10 a.m., for every station on every working weekday it
-- was in service (zeros included, so quiet mornings are not missing from the data)
CREATE OR REPLACE TABLE station_morning AS
WITH morning AS (
    SELECT * FROM trips_all
    WHERE ride_hour BETWEEN 7 AND 9
      AND ride_date IN (SELECT ride_date FROM workdays)
),
flows AS (
    SELECT ride_date, station_id, SUM(out_) AS bikes_out, SUM(in_) AS bikes_in
    FROM (SELECT ride_date, start_station_id AS station_id, 1 AS out_, 0 AS in_ FROM morning
          UNION ALL
          SELECT ride_date, end_station_id, 0, 1 FROM morning)
    GROUP BY ride_date, station_id
)
SELECT w.ride_date, s.station_id,
       COALESCE(f.bikes_out, 0) AS bikes_out,
       COALESCE(f.bikes_in, 0)  AS bikes_in
FROM workdays w
JOIN station_life s ON w.ride_date BETWEEN s.first_day AND s.last_day
LEFT JOIN flows f ON f.ride_date = w.ride_date AND f.station_id = s.station_id
ORDER BY w.ride_date, s.station_id;

-- Check: trips per year and rows in each table
SELECT 'Trips 2025' AS item, COUNT(*) AS n FROM trips_all WHERE year(start_time) = 2025
UNION ALL SELECT 'Trips 2026 (Jan-Sep)', COUNT(*) FROM trips_all WHERE year(start_time) = 2026
UNION ALL SELECT 'Hours in system_hourly', COUNT(*) FROM system_hourly
UNION ALL SELECT 'Working weekdays', COUNT(*) FROM workdays
UNION ALL SELECT 'Station-mornings', COUNT(*) FROM station_morning
UNION ALL SELECT 'Stations', COUNT(DISTINCT station_id) FROM station_morning;
