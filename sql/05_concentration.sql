-- 05. How unequal is demand across stations?
-- Splits stations into ten equal-sized groups by departures (NTILE) and shows each group's
-- share of all trips: if demand were even, every group would have 10%.

WITH station_trips AS (
    SELECT start_station_id AS station_id, COUNT(*) AS departures
    FROM trips
    GROUP BY start_station_id
),
deciles AS (
    SELECT station_id, departures,
           NTILE(10) OVER (ORDER BY departures DESC) AS decile
    FROM station_trips
)
SELECT
    decile                                                    AS station_group,
    CASE decile WHEN 1 THEN 'Busiest 10% of stations'
                WHEN 10 THEN 'Quietest 10% of stations'
                ELSE 'Group ' || decile END                   AS description,
    COUNT(*)                                                  AS stations,
    SUM(departures)                                           AS departures,
    ROUND(100.0 * SUM(departures) / SUM(SUM(departures)) OVER (), 1) AS share_of_trips_pct,
    MEDIAN(departures)                                        AS median_departures_per_station
FROM deciles
GROUP BY decile
ORDER BY decile;
