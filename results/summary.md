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
 Weekday     Casual     0              102.1               1.4
 Weekday     Casual     1               56.9               0.8
 Weekday     Casual     2               38.9               0.5
 Weekday     Casual     3               19.1               0.3
 Weekday     Casual     4               13.8               0.2
 Weekday     Casual     5               29.0               0.4
 Weekday     Casual     6               68.7               1.0
 Weekday     Casual     7              139.6               1.9
 Weekday     Casual     8              316.2               4.4
 Weekday     Casual     9              226.5               3.1
 Weekday     Casual    10              211.3               2.9
 Weekday     Casual    11              279.8               3.9
 Weekday     Casual    12              338.2               4.7
 Weekday     Casual    13              380.1               5.3
 Weekday     Casual    14              419.2               5.8
 Weekday     Casual    15              471.8               6.6
 Weekday     Casual    16              593.5               8.3
 Weekday     Casual    17              796.0              11.1
 Weekday     Casual    18              738.7              10.3
 Weekday     Casual    19              598.3               8.3
 Weekday     Casual    20              468.2               6.5
 Weekday     Casual    21              362.8               5.0
 Weekday     Casual    22              289.5               4.0
 Weekday     Casual    23              233.3               3.2
 Weekday     Member     0              175.1               1.0
 Weekday     Member     1               86.6               0.5
 Weekday     Member     2               56.5               0.3
 Weekday     Member     3               32.3               0.2
 Weekday     Member     4               40.9               0.2
 Weekday     Member     5              114.4               0.6
 Weekday     Member     6              335.1               1.8
 Weekday     Member     7              770.9               4.2
 Weekday     Member     8             1665.2               9.1
 Weekday     Member     9              977.4               5.4
 Weekday     Member    10              609.3               3.3
 Weekday     Member    11              660.9               3.6
 Weekday     Member    12              789.4               4.3
 Weekday     Member    13              794.4               4.4
 Weekday     Member    14              824.4               4.5
 Weekday     Member    15             1011.2               5.5
 Weekday     Member    16             1555.7               8.5
 Weekday     Member    17             2180.1              12.0
 Weekday     Member    18             1692.9               9.3
 Weekday     Member    19             1221.7               6.7
 Weekday     Member    20              945.5               5.2
 Weekday     Member    21              747.3               4.1
 Weekday     Member    22              566.8               3.1
 Weekday     Member    23              387.9               2.1
 Weekend     Casual     0              243.2               2.6
 Weekend     Casual     1              179.5               1.9
 Weekend     Casual     2              164.7               1.7
 Weekend     Casual     3               86.8               0.9
 Weekend     Casual     4               38.4               0.4
 Weekend     Casual     5               24.7               0.3
 Weekend     Casual     6               45.1               0.5
 Weekend     Casual     7               76.6               0.8
 Weekend     Casual     8              135.6               1.4
 Weekend     Casual     9              242.5               2.6
 Weekend     Casual    10              372.5               3.9
 Weekend     Casual    11              503.2               5.3
 Weekend     Casual    12              596.3               6.3
 Weekend     Casual    13              663.2               7.0
 Weekend     Casual    14              747.9               7.9
 Weekend     Casual    15              787.9               8.3
 Weekend     Casual    16              785.6               8.3
 Weekend     Casual    17              795.5               8.4
 Weekend     Casual    18              778.8               8.2
 Weekend     Casual    19              691.4               7.3
 Weekend     Casual    20              527.7               5.6
 Weekend     Casual    21              369.9               3.9
 Weekend     Casual    22              303.2               3.2
 Weekend     Casual    23              302.8               3.2
 Weekend     Member     0              341.1               2.4
 Weekend     Member     1              232.3               1.7
 Weekend     Member     2              180.7               1.3
 Weekend     Member     3               98.3               0.7
 Weekend     Member     4               56.2               0.4
 Weekend     Member     5               57.6               0.4
 Weekend     Member     6              124.9               0.9
 Weekend     Member     7              220.2               1.6
 Weekend     Member     8              374.5               2.7
 Weekend     Member     9              590.8               4.2
 Weekend     Member    10              766.2               5.5
 Weekend     Member    11              881.0               6.3
 Weekend     Member    12              953.9               6.8
 Weekend     Member    13              991.1               7.1
 Weekend     Member    14             1039.4               7.4
 Weekend     Member    15             1064.8               7.6
 Weekend     Member    16             1084.6               7.7
 Weekend     Member    17             1037.5               7.4
 Weekend     Member    18              993.2               7.1
 Weekend     Member    19              860.2               6.1
 Weekend     Member    20              678.6               4.8
 Weekend     Member    21              541.0               3.9
 Weekend     Member    22              456.8               3.3
 Weekend     Member    23              383.8               2.7
```

## 04. Which stations are busiest, and how concentrated is demand?

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
    pattern                              station_name  bikes_out_per_morning  bikes_in_per_morning  net_bikes_per_morning
Empties out               Fort York Blvd / Capreol Ct                   27.0                   5.6                  -21.5
Empties out                  Bathurst St / Front St W                   22.8                   4.6                  -18.2
Empties out                               Lisgar Park                   19.8                   4.1                  -15.7
Empties out                  Church St / Alexander St                   18.6                   5.1                  -13.5
Empties out            Dundas St E / Regent Park Blvd                   22.6                   9.5                  -13.1
Empties out                           144 Harrison St                   15.1                   2.2                  -12.9
Empties out        Western Battery Rd / Pirandello St                   13.9                   1.1                  -12.7
Empties out           Dan Leckie Way / Fort York Blvd                   14.9                   2.3                  -12.7
Empties out                       Mill St / Cherry St                   18.4                   5.8                  -12.6
Empties out               Spadina Ave / Blue Jays Way                   15.2                   2.6                  -12.5
   Fills up                     Elizabeth St / Elm St                   15.1                  33.6                   18.5
   Fills up                   York St / Queens Quay W                   16.3                  35.3                   19.0
   Fills up                        Bay St / Albert St                    2.8                  23.9                   21.2
   Fills up                King St W / University Ave                    2.9                  32.0                   29.1
   Fills up                  Wellington St W / Bay St                    2.5                  41.7                   39.2
   Fills up          Front St W / Bay St (South Side)                   11.9                  56.5                   44.6
   Fills up University Ave / Gerrard St W (East Side)                    9.4                  82.5                   73.1
   Fills up                    Adelaide St W / Bay St                    1.7                  92.1                   90.4
   Fills up                     Temperance St Station                    2.3                 107.3                  104.9
   Fills up            King St W / Bay St (West Side)                    2.5                 184.9                  182.4
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
Weekday 7-10 a.m.           2              Grand Avenue Park      Windsor St / Newcastle St    790              55.2             5.3
Weekday 7-10 a.m.           3       King St W / Charlotte St King St W / Bay St (West Side)    780              19.4             5.1
Weekday 7-10 a.m.           4    John St / Mercer St - SMART King St W / Bay St (West Side)    539              21.7             4.2
Weekday 7-10 a.m.           5     Front St W / Blue Jays Way                  Union Station    536               9.3             3.8
Weekday 7-10 a.m.           6    Spadina Ave / Adelaide St W         Adelaide St W / Bay St    510              23.9             6.9
Weekday 7-10 a.m.           7       Frederick St / King St E King St W / Bay St (West Side)    506              16.2             5.3
Weekday 7-10 a.m.           8       Bathurst St / Front St W King St W / Bay St (West Side)    494              10.7             9.7
Weekday 7-10 a.m.           9      Widmer St / Adelaide St W         Adelaide St W / Bay St    482              24.1             5.6
Weekday 7-10 a.m.          10 Niagara St / King St W - SMART King St W / Bay St (West Side)    443              14.2            10.0
```

## 08. How do members and casual riders use the system differently?

```
rider_type   trips  share_of_trips_pct  median_minutes  p90_minutes  longer_than_30_min_pct  round_trip_pct  weekend_pct  ebike_pct
    Member 4649847                68.5            10.6         24.2                     5.0             1.6         23.5       19.5
    Casual 2140442                31.5            15.5         55.3                    23.0             6.9         34.5       24.8
```
