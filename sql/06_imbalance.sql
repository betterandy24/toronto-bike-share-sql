-- 06. Which stations empty out or fill up during the weekday morning rush?
-- For each station, compares bikes taken out with bikes returned between 7 and 10 a.m. on
-- weekdays (public holidays excluded). A large negative "net" means riders leave with bikes
-- and few come back, so the station risks running out of bikes; a large positive net means
-- it risks running out of free docks. Ranked on the May-September riding season, when the
-- problem is largest; the January-April figure is shown alongside for comparison.

WITH morning AS (
    SELECT *,
           CASE WHEN month(ride_date) BETWEEN 5 AND 9 THEN 'peak' ELSE 'off_peak' END AS season
    FROM trips
    WHERE day_type = 'Weekday' AND ride_hour BETWEEN 7 AND 9
),
n_days AS (
    SELECT season, COUNT(DISTINCT ride_date) AS weekdays FROM morning GROUP BY season
),
flows AS (
    SELECT station_id, season,
           SUM(departures) AS departures,
           SUM(arrivals)   AS arrivals
    FROM (
        SELECT start_station_id AS station_id, season, 1 AS departures, 0 AS arrivals FROM morning
        UNION ALL
        SELECT end_station_id, season, 0, 1 FROM morning
    )
    GROUP BY station_id, season
),
per_day AS (
    SELECT f.station_id, f.season,
           f.departures * 1.0 / n.weekdays                 AS departures_per_day,
           f.arrivals * 1.0 / n.weekdays                   AS arrivals_per_day,
           (f.arrivals - f.departures) * 1.0 / n.weekdays  AS net_per_day
    FROM flows f JOIN n_days n USING (season)
),
scored AS (
    SELECT pk.*,
           op.net_per_day                                  AS net_off_peak,
           RANK() OVER (ORDER BY pk.net_per_day ASC)       AS empties_rank,
           RANK() OVER (ORDER BY pk.net_per_day DESC)      AS fills_rank
    FROM per_day pk
    LEFT JOIN per_day op ON op.station_id = pk.station_id AND op.season = 'off_peak'
    WHERE pk.season = 'peak'
)
SELECT
    CASE WHEN empties_rank <= 10 THEN 'Empties out' ELSE 'Fills up' END AS pattern,
    s.station_name,
    ROUND(departures_per_day, 1)          AS bikes_out_per_morning,
    ROUND(arrivals_per_day, 1)            AS bikes_in_per_morning,
    ROUND(net_per_day, 1)                 AS net_bikes_per_morning,
    ROUND(COALESCE(net_off_peak, 0), 1)   AS net_jan_apr
FROM scored
LEFT JOIN stations s USING (station_id)
WHERE empties_rank <= 10 OR fills_rank <= 10
ORDER BY net_per_day;
