-- 04. Which stations are busiest, and how concentrated is demand?
-- Ranks stations by departures (RANK), shows each station's share and the running total
-- (SUM OVER), and the casual-rider share at each station.

WITH station_trips AS (
    SELECT
        start_station_id                                 AS station_id,
        COUNT(*)                                         AS departures,
        COUNT(*) FILTER (WHERE rider_type = 'Casual')    AS casual_departures
    FROM trips
    GROUP BY start_station_id
),
ranked AS (
    SELECT
        station_id,
        departures,
        casual_departures,
        RANK() OVER (ORDER BY departures DESC)                              AS station_rank,
        100.0 * departures / SUM(departures) OVER ()                        AS share_pct,
        100.0 * SUM(departures) OVER (ORDER BY departures DESC, station_id
                                      ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW)
              / SUM(departures) OVER ()                                     AS cumulative_share_pct,
        COUNT(*) OVER ()                                                    AS n_stations
    FROM station_trips
)
SELECT
    r.station_rank,
    s.station_name,
    r.departures,
    ROUND(r.share_pct, 2)                                AS share_of_all_trips_pct,
    ROUND(r.cumulative_share_pct, 1)                     AS cumulative_share_pct,
    ROUND(100.0 * r.casual_departures / r.departures, 1) AS casual_share_pct,
    r.n_stations
FROM ranked r
LEFT JOIN stations s USING (station_id)
WHERE r.station_rank <= 15
ORDER BY r.station_rank;
