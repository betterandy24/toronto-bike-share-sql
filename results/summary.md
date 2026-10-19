# Query results

## 01. Load and clean the trip records

```
                                        step   trips
                        Records in the files 6830174
              Missing a start or end station   12951
                Start time could not be read       0
Shorter than 1 minute or longer than 3 hours   26934
                     Trips kept for analysis 6790289
```

## 02. How does ridership change through the year?

```
  month   trips  member_trips  casual_trips  casual_share_pct  median_minutes  change_vs_prev_month_pct
2026-01  136001        124053         11948               8.8             9.6                       NaN
2026-02  111689        102526          9163               8.2             9.8                     -17.9
2026-03  300243        260913         39330              13.1             9.8                     168.8
2026-04  516392        410846        105546              20.4            10.6                      72.0
2026-05  849727        597223        252504              29.7            11.9                      64.6
2026-06 1165388        763666        401722              34.5            12.5                      37.1
2026-07 1255978        806257        449721              35.8            12.1                       7.8
2026-08 1257700        792106        465594              37.0            12.4                       0.1
2026-09 1197171        792257        404914              33.8            11.7                      -4.8
```

## 03. When during the day do people ride?

```
       day_type rider_type  hour  avg_trips_per_day  share_of_day_pct
        Weekday     Casual     0               98.3               1.4
        Weekday     Casual     1               54.5               0.8
        Weekday     Casual     2               36.8               0.5
        Weekday     Casual     3               17.5               0.3
        Weekday     Casual     4               13.2               0.2
        Weekday     Casual     5               29.3               0.4
        Weekday     Casual     6               70.0               1.0
        Weekday     Casual     7              142.1               2.0
        Weekday     Casual     8              323.3               4.6
        Weekday     Casual     9              225.9               3.2
        Weekday     Casual    10              202.8               2.9
        Weekday     Casual    11              265.7               3.8
        Weekday     Casual    12              320.1               4.6
        Weekday     Casual    13              358.1               5.1
        Weekday     Casual    14              394.7               5.6
        Weekday     Casual    15              445.5               6.4
        Weekday     Casual    16              572.6               8.2
        Weekday     Casual    17              783.2              11.2
        Weekday     Casual    18              727.3              10.4
        Weekday     Casual    19              586.0               8.4
        Weekday     Casual    20              459.5               6.6
        Weekday     Casual    21              356.4               5.1
        Weekday     Casual    22              285.3               4.1
        Weekday     Casual    23              230.3               3.3
        Weekday     Member     0              171.9               0.9
        Weekday     Member     1               84.6               0.5
        Weekday     Member     2               54.3               0.3
        Weekday     Member     3               31.2               0.2
        Weekday     Member     4               40.8               0.2
        Weekday     Member     5              116.7               0.6
        Weekday     Member     6              343.1               1.9
        Weekday     Member     7              792.0               4.3
        Weekday     Member     8             1714.9               9.3
        Weekday     Member     9              994.5               5.4
        Weekday     Member    10              605.0               3.3
        Weekday     Member    11              650.9               3.5
        Weekday     Member    12              781.8               4.3
        Weekday     Member    13              783.9               4.3
        Weekday     Member    14              811.5               4.4
        Weekday     Member    15             1003.6               5.5
        Weekday     Member    16             1569.5               8.5
        Weekday     Member    17             2216.6              12.1
        Weekday     Member    18             1712.9               9.3
        Weekday     Member    19             1231.5               6.7
        Weekday     Member    20              952.8               5.2
        Weekday     Member    21              752.3               4.1
        Weekday     Member    22              569.1               3.1
        Weekday     Member    23              388.1               2.1
Weekend/holiday     Casual     0              240.1               2.5
Weekend/holiday     Casual     1              174.8               1.8
Weekend/holiday     Casual     2              158.9               1.6
Weekend/holiday     Casual     3               84.8               0.9
Weekend/holiday     Casual     4               37.7               0.4
Weekend/holiday     Casual     5               24.3               0.3
Weekend/holiday     Casual     6               44.3               0.5
Weekend/holiday     Casual     7               76.2               0.8
Weekend/holiday     Casual     8              134.8               1.4
Weekend/holiday     Casual     9              242.3               2.5
Weekend/holiday     Casual    10              378.1               3.9
Weekend/holiday     Casual    11              516.0               5.3
Weekend/holiday     Casual    12              615.0               6.3
Weekend/holiday     Casual    13              688.5               7.1
Weekend/holiday     Casual    14              775.0               8.0
Weekend/holiday     Casual    15              820.0               8.5
Weekend/holiday     Casual    16              815.9               8.4
Weekend/holiday     Casual    17              823.7               8.5
Weekend/holiday     Casual    18              800.9               8.3
Weekend/holiday     Casual    19              710.9               7.3
Weekend/holiday     Casual    20              542.0               5.6
Weekend/holiday     Casual    21              383.5               4.0
Weekend/holiday     Casual    22              311.4               3.2
Weekend/holiday     Casual    23              303.7               3.1
Weekend/holiday     Member     0              334.5               2.4
Weekend/holiday     Member     1              224.7               1.6
Weekend/holiday     Member     2              175.2               1.2
Weekend/holiday     Member     3               95.3               0.7
Weekend/holiday     Member     4               55.2               0.4
Weekend/holiday     Member     5               57.2               0.4
Weekend/holiday     Member     6              124.5               0.9
Weekend/holiday     Member     7              218.8               1.6
Weekend/holiday     Member     8              371.0               2.6
Weekend/holiday     Member     9              584.7               4.2
Weekend/holiday     Member    10              762.8               5.4
Weekend/holiday     Member    11              885.1               6.3
Weekend/holiday     Member    12              956.9               6.8
Weekend/holiday     Member    13              998.1               7.1
Weekend/holiday     Member    14             1050.2               7.5
Weekend/holiday     Member    15             1077.2               7.7
Weekend/holiday     Member    16             1093.0               7.8
Weekend/holiday     Member    17             1050.9               7.5
Weekend/holiday     Member    18             1006.6               7.2
Weekend/holiday     Member    19              868.2               6.2
Weekend/holiday     Member    20              684.5               4.9
Weekend/holiday     Member    21              546.9               3.9
Weekend/holiday     Member    22              460.9               3.3
Weekend/holiday     Member    23              383.7               2.7
```

## 04. Which stations are busiest?

```
 station_rank                            station_name  departures  share_of_all_trips_pct  cumulative_share_pct  casual_share_pct  n_stations
            1                Centre Island Ferry Dock       87490                    1.29                   1.3              96.0        1098
            2                 York St / Queens Quay W       48037                    0.71                   2.0              43.2        1098
            3                Ward's Island Ferry Dock       44030                    0.65                   2.6              91.0        1098
            4                           Centre Island       37276                    0.55                   3.2              93.0        1098
            5         Bay St / College St (East Side)       36137                    0.53                   3.7              19.7        1098
            6               Widmer St / Adelaide St W       34366                    0.51                   4.2              28.0        1098
            6                 King St W / Portland St       34366                    0.51                   4.7              29.2        1098
            8               Hanlan's Point Ferry Dock       33941                    0.50                   5.2              80.4        1098
            9                    Queen St W / John St       32840                    0.48                   5.7              26.4        1098
           10 Bay St / Queens Quay W (Ferry Terminal)       32177                    0.47                   6.2              47.4        1098
           11                   Toronto Inukshuk Park       30911                    0.46                   6.7              55.9        1098
           12                   College St / Major St       30718                    0.45                   7.1              26.4        1098
           13               Dundas St W / Crawford St       30578                    0.45                   7.6              34.0        1098
           14         Queens Quay E / Lower Jarvis St       29925                    0.44                   8.0              41.8        1098
           15                 College St / Markham St       28631                    0.42                   8.4              27.8        1098
```

## 05. How unequal is demand across stations?

```
 station_group              description  stations  departures  share_of_trips_pct  median_departures_per_station
             1  Busiest 10% of stations       110   2645765.0                39.0                        21906.0
             2                  Group 2       110   1516950.0                22.3                        13757.0
             3                  Group 3       110   1038452.0                15.3                         9394.5
             4                  Group 4       110    693906.0                10.2                         6189.5
             5                  Group 5       110    431888.0                 6.4                         3978.0
             6                  Group 6       110    243257.0                 3.6                         2063.0
             7                  Group 7       110    129611.0                 1.9                         1180.5
             8                  Group 8       110     57711.0                 0.8                          497.5
             9                  Group 9       109     23547.0                 0.3                          211.0
            10 Quietest 10% of stations       109      9202.0                 0.1                           92.0
```

## 06. Which stations empty out or fill up during the weekday morning rush?

```
    pattern                              station_name  bikes_out_per_morning  bikes_in_per_morning  net_bikes_per_morning  net_jan_apr
Empties out               Fort York Blvd / Capreol Ct                   39.2                   7.6                  -31.5        -10.3
Empties out                  Bathurst St / Front St W                   31.3                   6.7                  -24.6        -11.5
Empties out                               Lisgar Park                   29.2                   5.9                  -23.3         -6.8
Empties out                           144 Harrison St                   24.4                   3.6                  -20.9         -3.7
Empties out                         439 Sherbourne St                   23.6                   3.6                  -20.0         -3.8
Empties out        Western Battery Rd / Pirandello St                   21.8                   1.9                  -20.0         -4.5
Empties out                       Mill St / Cherry St                   28.3                   8.6                  -19.7         -4.3
Empties out           Dan Leckie Way / Fort York Blvd                   23.0                   3.5                  -19.5         -5.0
Empties out                  Church St / Alexander St                   26.1                   6.9                  -19.2         -7.1
Empties out               Spadina Ave / Blue Jays Way                   22.5                   4.1                  -18.4         -6.0
   Fills up                   York St / Queens Quay W                   24.9                  53.2                   28.3          8.4
   Fills up                     Simcoe St / Pullan Pl                    8.6                  37.1                   28.5          6.0
   Fills up                        Bay St / Albert St                    3.7                  35.0                   31.3          9.8
   Fills up                King St W / University Ave                    4.5                  49.1                   44.6         11.8
   Fills up                  Wellington St W / Bay St                    3.8                  65.3                   61.5         14.0
   Fills up          Front St W / Bay St (South Side)                   18.0                  79.6                   61.6         26.2
   Fills up University Ave / Gerrard St W (East Side)                   13.9                 123.6                  109.6         32.5
   Fills up                     Temperance St Station                    3.5                 151.9                  148.5         58.3
   Fills up                    Adelaide St W / Bay St                    2.6                 152.8                  150.1         22.2
   Fills up            King St W / Bay St (West Side)                    3.8                 277.0                  273.2         82.7
```

## 07. What are the most popular routes, and who rides them?

```
        view_name  route_rank                   from_station                     to_station  trips  casual_share_pct  median_minutes
        All trips           1       Centre Island Ferry Dock       Ward's Island Ferry Dock  17814              94.2            48.1
        All trips           2       Centre Island Ferry Dock                  Centre Island  10328              94.7            44.4
        All trips           3                  Centre Island       Ward's Island Ferry Dock  10202              90.7            29.0
        All trips           4       Ward's Island Ferry Dock       Centre Island Ferry Dock  10107              94.5            41.7
        All trips           5                  Centre Island       Centre Island Ferry Dock   9624              96.2            43.4
        All trips           6       Ward's Island Ferry Dock                  Centre Island   9356              89.8            30.0
        All trips           7      Hanlan's Point Ferry Dock           Hanlan's Point Beach   8800              60.6             6.1
        All trips           8       Centre Island Ferry Dock      Hanlan's Point Ferry Dock   8414              96.2            55.7
        All trips           9      Hanlan's Point Ferry Dock       Ward's Island Ferry Dock   6437              91.4            59.4
        All trips          10           Hanlan's Point Beach      Hanlan's Point Ferry Dock   6364              63.7             6.1
Weekday 7-10 a.m.           1        King St W / Portland St King St W / Bay St (West Side)    994              18.5             7.3
Weekday 7-10 a.m.           2              Grand Avenue Park      Windsor St / Newcastle St    789              55.1             5.3
Weekday 7-10 a.m.           3       King St W / Charlotte St King St W / Bay St (West Side)    779              19.3             5.1
Weekday 7-10 a.m.           4    John St / Mercer St - SMART King St W / Bay St (West Side)    539              21.7             4.2
Weekday 7-10 a.m.           5     Front St W / Blue Jays Way                  Union Station    535               9.3             3.8
Weekday 7-10 a.m.           6    Spadina Ave / Adelaide St W         Adelaide St W / Bay St    510              23.9             6.9
Weekday 7-10 a.m.           7       Frederick St / King St E King St W / Bay St (West Side)    506              16.2             5.3
Weekday 7-10 a.m.           8       Bathurst St / Front St W King St W / Bay St (West Side)    494              10.7             9.7
Weekday 7-10 a.m.           9      Widmer St / Adelaide St W         Adelaide St W / Bay St    482              24.1             5.6
Weekday 7-10 a.m.          10 Niagara St / King St W - SMART King St W / Bay St (West Side)    443              14.2            10.0
```

## 08. How do members and casual riders use the system differently?

```
rider_type   trips  share_of_trips_pct  median_minutes  p90_minutes  longer_than_30_min_pct  round_trip_pct  weekend_holiday_pct  ebike_pct
    Member 4649847                68.5            10.6         24.2                     5.0             1.6                 25.7       19.5
    Casual 2140442                31.5            15.5         55.3                    23.0             6.9                 38.5       24.8
```

## 09. Spotlight: why is Grand Avenue Park -> Windsor St / Newcastle St a top morning route?

```
                                     direction            time_window  trips  casual_pct  median_minutes  ebike_pct  trips_jan_apr  trips_may_sep  days_with_trips
Grand Avenue Park -> Windsor St / Newcastle St    1 Weekday 7-10 a.m.    789        55.1             5.3       10.3            117            672              157
Grand Avenue Park -> Windsor St / Newcastle St     2 Weekday 4-7 p.m.    126        57.1             5.0       15.9             18            108               79
Grand Avenue Park -> Windsor St / Newcastle St 3 Weekday, other hours    283        78.4             5.0       20.8             37            246              123
Grand Avenue Park -> Windsor St / Newcastle St      4 Weekend/holiday    210        57.6             5.4       13.3             32            178               58
Windsor St / Newcastle St -> Grand Avenue Park    1 Weekday 7-10 a.m.      8        50.0             5.8       12.5              1              7                8
Windsor St / Newcastle St -> Grand Avenue Park     2 Weekday 4-7 p.m.    633        65.6             5.1        6.5             87            546              147
Windsor St / Newcastle St -> Grand Avenue Park 3 Weekday, other hours    408        65.7             5.0       15.9             68            340              142
Windsor St / Newcastle St -> Grand Avenue Park      4 Weekend/holiday    199        59.8             6.0       10.6             21            178               55
```
