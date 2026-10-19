-- 06. Which stations empty out or fill up during the weekday morning rush?
-- For each station, compares bikes taken out with bikes returned between 7 and 10 a.m. on
-- weekdays. A large negative "net" means riders leave with bikes and few come back, so the
-- station risks running out of bikes; a large positive net means it risks running out of
-- free docks. These are the stations an operator would rebalance first.

WITH morning AS (
    SELECT * FROM trips
    WHERE day_type = 'Weekday' AND ride_hour BETWEEN 7 AND 9
),
n_days AS (
    SELECT COUNT(DISTINCT ride_date) AS weekdays FROM morning
),
flows AS (
    SELECT station_id,
           SUM(departures) AS departures,
           SUM(arrivals)   AS arrivals
    FROM (
        SELECT start_station_id AS station_id, 1 AS departures, 0 AS arrivals FROM morning
        UNION ALL
        SELECT end_station_id, 0, 1 FROM morning
    )
    GROUP BY station_id
),
scored AS (
    SELECT
        f.station_id,
        f.departures * 1.0 / n.weekdays                   AS departures_per_day,
        f.arrivals * 1.0 / n.weekdays                     AS arrivals_per_day,
        (f.arrivals - f.departures) * 1.0 / n.weekdays    AS net_per_day,
        RANK() OVER (ORDER BY f.arrivals - f.departures ASC)  AS empties_rank,
        RANK() OVER (ORDER BY f.arrivals - f.departures DESC) AS fills_rank
    FROM flows f CROSS JOIN n_days n
)
SELECT
    CASE WHEN empties_rank <= 10 THEN 'Empties out' ELSE 'Fills up' END AS pattern,
    s.station_name,
    ROUND(departures_per_day, 1)  AS bikes_out_per_morning,
    ROUND(arrivals_per_day, 1)    AS bikes_in_per_morning,
    ROUND(net_per_day, 1)         AS net_bikes_per_morning
FROM scored
LEFT JOIN stations s USING (station_id)
WHERE empties_rank <= 10 OR fills_rank <= 10
ORDER BY net_per_day;
