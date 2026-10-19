-- 02. How does ridership change through the year?
-- Trips per month by rider type, the casual share, typical trip length,
-- and the change from the previous month (window function LAG).

WITH monthly AS (
    SELECT
        ride_month,
        COUNT(*)                                        AS trips,
        COUNT(*) FILTER (WHERE rider_type = 'Member')   AS member_trips,
        COUNT(*) FILTER (WHERE rider_type = 'Casual')   AS casual_trips,
        MEDIAN(duration_min)                            AS median_minutes
    FROM trips
    GROUP BY ride_month
)
SELECT
    strftime(ride_month, '%Y-%m')                                   AS month,
    trips,
    member_trips,
    casual_trips,
    ROUND(100.0 * casual_trips / trips, 1)                          AS casual_share_pct,
    ROUND(median_minutes, 1)                                        AS median_minutes,
    ROUND(100.0 * (trips - LAG(trips) OVER (ORDER BY ride_month))
          / LAG(trips) OVER (ORDER BY ride_month), 1)               AS change_vs_prev_month_pct
FROM monthly
ORDER BY ride_month;
