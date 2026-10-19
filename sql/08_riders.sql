-- 08. How do members and casual riders use the system differently?
-- Trip counts, typical and long trip lengths (percentiles), the share of round trips and
-- the share of rides taken at weekends or public holidays, or on e-bikes (EFIT models), by
-- rider type.

SELECT
    rider_type,
    COUNT(*)                                                         AS trips,
    ROUND(100.0 * COUNT(*) / SUM(COUNT(*)) OVER (), 1)               AS share_of_trips_pct,
    ROUND(MEDIAN(duration_min), 1)                                   AS median_minutes,
    ROUND(QUANTILE_CONT(duration_min, 0.9), 1)                       AS p90_minutes,
    ROUND(100.0 * AVG(CASE WHEN duration_min > 30 THEN 1 ELSE 0 END), 1)
                                                                     AS longer_than_30_min_pct,
    ROUND(100.0 * AVG(CASE WHEN start_station_id = end_station_id THEN 1 ELSE 0 END), 1)
                                                                     AS round_trip_pct,
    ROUND(100.0 * AVG(CASE WHEN day_type = 'Weekend/holiday' THEN 1 ELSE 0 END), 1)
                                                                     AS weekend_holiday_pct,
    ROUND(100.0 * AVG(CASE WHEN bike_type = 'E-bike' THEN 1 ELSE 0 END), 1)
                                                                     AS ebike_pct
FROM trips
WHERE rider_type IN ('Member', 'Casual')
GROUP BY rider_type
ORDER BY trips DESC;
