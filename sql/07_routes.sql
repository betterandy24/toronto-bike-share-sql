-- 07. What are the most popular routes, and who rides them?
-- Top station-to-station routes (round trips excluded) in two views: all trips, and weekday
-- morning trips (7-10 a.m., public holidays excluded), which are mostly commutes. Station names come from two joins
-- to the station list. Shows the casual share and typical trip length on each route.

WITH tagged AS (
    SELECT *, 'All trips' AS view_name FROM trips
    UNION ALL
    SELECT *, 'Weekday 7-10 a.m.' FROM trips
    WHERE day_type = 'Weekday' AND ride_hour BETWEEN 7 AND 9
),
routes AS (
    SELECT
        view_name,
        start_station_id,
        end_station_id,
        COUNT(*)                                          AS trips,
        COUNT(*) FILTER (WHERE rider_type = 'Casual')     AS casual_trips,
        MEDIAN(duration_min)                              AS median_minutes
    FROM tagged
    WHERE start_station_id <> end_station_id
    GROUP BY view_name, start_station_id, end_station_id
),
ranked AS (
    SELECT *, ROW_NUMBER() OVER (PARTITION BY view_name ORDER BY trips DESC) AS route_rank
    FROM routes
)
SELECT
    view_name,
    route_rank,
    a.station_name                                      AS from_station,
    b.station_name                                      AS to_station,
    trips,
    ROUND(100.0 * casual_trips / trips, 1)              AS casual_share_pct,
    ROUND(median_minutes, 1)                            AS median_minutes
FROM ranked r
LEFT JOIN stations a ON a.station_id = r.start_station_id
LEFT JOIN stations b ON b.station_id = r.end_station_id
WHERE route_rank <= 10
ORDER BY view_name, route_rank;
