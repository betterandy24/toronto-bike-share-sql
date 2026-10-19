-- 09. Spotlight: why is Grand Avenue Park -> Windsor St / Newcastle St a top morning route?
-- It is the second-busiest weekday-morning route, yet most of its riders are casual and the
-- ride takes about 5 minutes, unlike the other commute routes. This breaks the route down
-- by direction and time of day, to see whether it behaves like a commute (out in the
-- morning, back in the evening) and when in the year it is used.

WITH ends AS (
    SELECT station_id, station_name FROM stations
    WHERE station_name IN ('Grand Avenue Park', 'Windsor St / Newcastle St')
),
route AS (
    SELECT t.*,
           a.station_name || ' -> ' || b.station_name AS direction,
           CASE WHEN t.day_type = 'Weekday' AND t.ride_hour BETWEEN 7 AND 9   THEN '1 Weekday 7-10 a.m.'
                WHEN t.day_type = 'Weekday' AND t.ride_hour BETWEEN 16 AND 18 THEN '2 Weekday 4-7 p.m.'
                WHEN t.day_type = 'Weekday'                                    THEN '3 Weekday, other hours'
                ELSE '4 Weekend/holiday' END                AS time_window
    FROM trips t
    JOIN ends a ON a.station_id = t.start_station_id
    JOIN ends b ON b.station_id = t.end_station_id
    WHERE t.start_station_id <> t.end_station_id
)
SELECT
    direction,
    time_window,
    COUNT(*)                                                         AS trips,
    ROUND(100.0 * AVG(CASE WHEN rider_type = 'Casual' THEN 1 ELSE 0 END), 1) AS casual_pct,
    ROUND(MEDIAN(duration_min), 1)                                   AS median_minutes,
    ROUND(100.0 * AVG(CASE WHEN bike_type = 'E-bike' THEN 1 ELSE 0 END), 1)  AS ebike_pct,
    COUNT(*) FILTER (WHERE month(ride_date) <= 4)                    AS trips_jan_apr,
    COUNT(*) FILTER (WHERE month(ride_date) >= 5)                    AS trips_may_sep,
    COUNT(DISTINCT ride_date)                                        AS days_with_trips
FROM route
GROUP BY direction, time_window
ORDER BY direction, time_window;
