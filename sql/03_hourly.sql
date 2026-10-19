-- 03. When during the day do people ride?
-- Average trips per hour on weekdays and on weekends/public holidays, separately for members and casual riders.
-- Dividing by the number of days of each type turns totals into a typical day.

WITH day_counts AS (
    SELECT day_type, COUNT(DISTINCT ride_date) AS n_days
    FROM trips
    GROUP BY day_type
),
hourly AS (
    SELECT day_type, rider_type, ride_hour, COUNT(*) AS trips
    FROM trips
    WHERE rider_type IN ('Member', 'Casual')
    GROUP BY day_type, rider_type, ride_hour
)
SELECT
    h.day_type,
    h.rider_type,
    h.ride_hour                                   AS hour,
    ROUND(h.trips * 1.0 / d.n_days, 1)            AS avg_trips_per_day,
    -- share of that rider type's daily trips that happen in this hour
    ROUND(100.0 * h.trips / SUM(h.trips) OVER (PARTITION BY h.day_type, h.rider_type), 1)
                                                  AS share_of_day_pct
FROM hourly h
JOIN day_counts d USING (day_type)
ORDER BY h.day_type, h.rider_type, h.ride_hour;
