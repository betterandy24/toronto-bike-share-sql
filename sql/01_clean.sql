-- 01. Load and clean the trip records
-- Reads every CSV in data/ as text (column names lower-cased, spaces -> underscores),
-- parses the timestamps, and keeps trips that are plausible rides. Works with the 2026
-- single-file layout and with older monthly files, whose column names and date format differ.

CREATE OR REPLACE VIEW raw_trips AS
SELECT *
FROM read_csv('data/*.csv',
              all_varchar     = true,    -- read everything as text, then convert explicitly
              union_by_name   = true,    -- monthly files may differ slightly in columns
              normalize_names = true,
              filename        = true);

CREATE OR REPLACE TABLE parsed_trips AS
SELECT
    trip_id,
    TRY_CAST(TRY_CAST(start_station_id AS DOUBLE) AS INTEGER) AS start_station_id,
    REGEXP_REPLACE(TRIM(start_station_name), '\s+', ' ', 'g') AS start_station_name,
    TRY_CAST(TRY_CAST(end_station_id AS DOUBLE) AS INTEGER) AS end_station_id,
    REGEXP_REPLACE(TRIM(end_station_name), '\s+', ' ', 'g') AS end_station_name,
    COALESCE(TRY_STRPTIME(start_time, '%m/%d/%Y %H:%M'),
             TRY_STRPTIME(start_time, '%m/%d/%Y %H:%M:%S'),
             TRY_STRPTIME(start_time, '%Y-%m-%d %H:%M:%S'))  AS start_time,
    COALESCE(TRY_STRPTIME(end_time, '%m/%d/%Y %H:%M'),
             TRY_STRPTIME(end_time, '%m/%d/%Y %H:%M:%S'),
             TRY_STRPTIME(end_time, '%Y-%m-%d %H:%M:%S'))    AS end_time,
    TRY_CAST(COLUMNS('^trip_+duration$') AS INTEGER)        AS duration_s,
    TRIM(user_type)                                         AS user_type,
    TRIM(COLUMNS('^(bike_)?model$'))                        AS bike_model
FROM raw_trips;

-- Ontario public holidays in January-September 2026 (including Toronto's Civic Holiday).
-- Commuting stops on these days, so they are grouped with weekends rather than weekdays.
CREATE OR REPLACE TABLE holidays AS
SELECT CAST(holiday_date AS DATE) AS holiday_date, holiday_name
FROM (VALUES ('2026-01-01', 'New Year''s Day'),
             ('2026-02-16', 'Family Day'),
             ('2026-04-03', 'Good Friday'),
             ('2026-05-18', 'Victoria Day'),
             ('2026-07-01', 'Canada Day'),
             ('2026-08-03', 'Civic Holiday'),
             ('2026-09-07', 'Labour Day')) AS t(holiday_date, holiday_name);

-- Keep trips with both stations, valid times and a duration between 1 minute and 3 hours.
-- Very short trips are usually a rider re-docking the same bike; very long ones are
-- usually bikes that were not returned properly.
CREATE OR REPLACE TABLE trips AS
SELECT
    trip_id,
    start_station_id,
    end_station_id,
    start_time,
    end_time,
    duration_s / 60.0                                  AS duration_min,
    -- 'Casual' is checked first because older files say 'Casual Member' / 'Annual Member'
    CASE WHEN user_type ILIKE '%casual%' THEN 'Casual'
         WHEN user_type ILIKE '%member%' OR user_type ILIKE '%annual%' THEN 'Member'
         ELSE 'Other' END                              AS rider_type,
    -- EFIT models are the e-bikes and ICONIC is the classic pedal bike; anything else
    -- (about 1% of 2026 trips, model ASTRO) is kept separate rather than guessed
    CASE WHEN bike_model ILIKE 'EFIT%'  THEN 'E-bike'
         WHEN bike_model ILIKE 'ICONIC' THEN 'Classic'
         ELSE 'Other model' END                        AS bike_type,
    CAST(start_time AS DATE)                           AS ride_date,
    date_trunc('month', start_time)                    AS ride_month,
    hour(start_time)                                   AS ride_hour,
    CASE WHEN dayofweek(start_time) IN (0, 6) OR h.holiday_date IS NOT NULL
         THEN 'Weekend/holiday' ELSE 'Weekday' END     AS day_type
FROM parsed_trips p
LEFT JOIN holidays h ON h.holiday_date = CAST(p.start_time AS DATE)
WHERE start_station_id IS NOT NULL
  AND end_station_id   IS NOT NULL
  AND start_time       IS NOT NULL
  AND duration_s BETWEEN 60 AND 3 * 3600;

-- One name per station: the name it appears under most often
CREATE OR REPLACE TABLE stations AS
SELECT station_id, mode(station_name) AS station_name
FROM (
    SELECT start_station_id AS station_id, start_station_name AS station_name FROM parsed_trips
    UNION ALL
    SELECT end_station_id, end_station_name FROM parsed_trips
)
WHERE station_id IS NOT NULL
GROUP BY station_id;

-- Data-quality summary: how many records were kept and why the others were dropped
SELECT 'Records in the files'                          AS step, COUNT(*) AS trips FROM parsed_trips
UNION ALL
SELECT 'Missing a start or end station',
       COUNT(*) FILTER (WHERE start_station_id IS NULL OR end_station_id IS NULL) FROM parsed_trips
UNION ALL
SELECT 'Start time could not be read',
       COUNT(*) FILTER (WHERE start_time IS NULL) FROM parsed_trips
UNION ALL
SELECT 'Shorter than 1 minute or longer than 3 hours',
       COUNT(*) FILTER (WHERE start_station_id IS NOT NULL AND end_station_id IS NOT NULL
                          AND start_time IS NOT NULL
                          AND (duration_s IS NULL OR duration_s NOT BETWEEN 60 AND 3 * 3600))
FROM parsed_trips
UNION ALL
SELECT 'Trips kept for analysis', COUNT(*) FROM trips;
