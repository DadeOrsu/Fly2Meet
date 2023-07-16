airport(lin).
airport(cdg).
airport(lgw).
airport(lcy).
airport(ory).
airport(lhr).
flight(ory, lin, az, 357, date(2023, 7, 27, 7, 30, 0, 3600, cest, true), date(2023, 7, 27, 8, 55, 0, 3600, cest, true), 5100, 159.43).
flight(ory, lin, az, 351, date(2023, 7, 27, 9, 10, 0, 3600, cest, true), date(2023, 7, 27, 10, 35, 0, 3600, cest, true), 5100, 159.43).
flight(cdg, lin, az, 305, date(2023, 7, 27, 9, 20, 0, 3600, cest, true), date(2023, 7, 27, 10, 50, 0, 3600, cest, true), 5400, 160.59).
flight(cdg, lin, az, 313, date(2023, 7, 27, 16, 55, 0, 3600, cest, true), date(2023, 7, 27, 18, 25, 0, 3600, cest, true), 5400, 188.59).
flight(cdg, lin, az, 315, date(2023, 7, 27, 19, 25, 0, 3600, cest, true), date(2023, 7, 27, 20, 55, 0, 3600, cest, true), 5400, 188.59).
flight(cdg, lin, az, 311, date(2023, 7, 27, 21, 30, 0, 3600, cest, true), date(2023, 7, 27, 23, 0, 0, 3600, cest, true), 5400, 188.59).
flight(cdg, lin, af, 1312, date(2023, 7, 27, 18, 20, 0, 3600, cest, true), date(2023, 7, 27, 19, 45, 0, 3600, cest, true), 5100, 193.87).
flight(cdg, lin, af, 1212, date(2023, 7, 27, 7, 20, 0, 3600, cest, true), date(2023, 7, 27, 8, 50, 0, 3600, cest, true), 5400, 193.87).
flight(cdg, lhr, af, 1180, date(2023, 7, 27, 18, 15, 0, 3600, cest, true), date(2023, 7, 27, 18, 35, 0, 0, bst, true), 4800, 137.87).
flight(cdg, lhr, af, 1280, date(2023, 7, 27, 16, 10, 0, 3600, cest, true), date(2023, 7, 27, 16, 35, 0, 0, bst, true), 5100, 137.87).
flight(cdg, lhr, af, 1380, date(2023, 7, 27, 20, 55, 0, 3600, cest, true), date(2023, 7, 27, 21, 20, 0, 0, bst, true), 5100, 137.87).
flight(cdg, lhr, af, 1580, date(2023, 7, 27, 10, 0, 0, 3600, cest, true), date(2023, 7, 27, 10, 30, 0, 0, bst, true), 5400, 137.87).
flight(cdg, lhr, af, 1680, date(2023, 7, 27, 7, 35, 0, 3600, cest, true), date(2023, 7, 27, 8, 0, 0, 0, bst, true), 5100, 137.87).
flight(ory, lgw, vy, 8942, date(2023, 7, 27, 6, 55, 0, 3600, cest, true), date(2023, 7, 27, 7, 0, 0, 0, bst, true), 3900, 148.43).



fly2Meet(Airport1, Airport2, SortStrategy, Flights) :-
    airport(Airport1), airport(Airport2), dif(Airport1, Airport2),
    findall(FCombo, findFlights(Airport1, Airport2, FCombo), TmpFlights),
    sortByStrategy(TmpFlights, SortStrategy, Flights),
    printFlights(Flights).

printFlights([]).
printFlights([sol(_, _, _, _, Flight1Info, Flight2Info)|Rest]) :-
    format("Flight 1: ~w~n", [Flight1Info]),
    format("Flight 2: ~w~n", [Flight2Info]),
    printFlights(Rest).

findFlights(Airport1, Airport2, sol(AvgPrice, AvgDuration, WaitingTime, Rank, Flight1Info, Flight2Info)) :-
    flight(Airport1, Airport3, CarrierNo13, FlightNo13, DepDate13, ArrDate13, Duration13, Price13),
    flight(Airport2, Airport3, CarrierNo23, FlightNo23, DepDate23, ArrDate23, Duration23, Price23),
    AvgPrice is (Price13 + Price23) / 2,
    AvgDuration is (Duration13 + Duration23) / 2,
    date_time_stamp(ArrDate13, ArrDate13ts),
    date_time_stamp(ArrDate23, ArrDate23ts),
    WaitingTime is abs(ArrDate23ts - ArrDate13ts),
    Rank is AvgPrice + AvgDuration + WaitingTime,
    Flight1Info = f(Airport1, Airport3, CarrierNo13, FlightNo13, DepDate13, ArrDate13, Duration13, Price13),
    Flight2Info = f(Airport2, Airport3, CarrierNo23, FlightNo23, DepDate23, ArrDate23, Duration23, Price23).

sortByStrategy(L, price, SortedL) :- sort(1, @=<, L, SortedL).
sortByStrategy(L, duration, SortedL) :- sort(2, @=<, L, SortedL).
sortByStrategy(L, waitingtime, SortedL) :- sort(3, @=<, L, SortedL).
sortByStrategy(L, bestsolution, SortedL) :- sort(4, @=<, L, SortedL).
