:- consult('prologFacts/prolog_facts.pl').

wPrice(AP) :- AP is 1/3.
wDuration(AD) :- AD is 1/3.
wWaitingTime(AWT) :- AWT is 1/3.


fly2meet(Airport1, Airport2, SortStrategy, Return, CapWT, SameAirport, Flights) :-
    airport(Airport1, _, _), airport(Airport2, _, _), dif(Airport1, Airport2),
    minAndMax(price, Return, MaxP, MinP),
    minAndMax(duration, Return, MaxD, MinD),
    setof(FCombo, eligibleFlights(Airport1, Airport2, MaxP, MinP, MaxD, MinD, Return, CapWT, SameAirport, FCombo), TmpFlights),
    sortByStrategy(TmpFlights, SortStrategy, Flights).

eligibleFlights(Airport1, Airport2, MaxP, MinP, MaxD, MinD, no, CapWT, yes, Solution) :-
    flight(Airport1, Airport3, CarrierNo13, FlightNo13, DepDate13, ArrDate13, Duration13, Price13),
    Flight1Info=f(Airport1, Airport3, CarrierNo13, FlightNo13, DepDate13, ArrDate13, Duration13, Price13),
    flight(Airport2, Airport3, CarrierNo23, FlightNo23, DepDate23, ArrDate23, Duration23, Price23),
    Flight2Info=f(Airport2, Airport3, CarrierNo23, FlightNo23, DepDate23, ArrDate23, Duration23, Price23),
    avg(Price13,Price23,AvgPrice),
    avg(Duration13,Duration23,AvgDuration),
    waitingTime(ArrDate13, DepDate23, WaitingTime), WaitingTime =< CapWT,
    travelScore(AvgPrice,AvgDuration,WaitingTime,MinP,MaxP,MinD,MaxD,CapWT,Rank),
    Solution=sol(AvgPrice, AvgDuration, WaitingTime, Rank, Flight1Info, Flight2Info).

eligibleFlights(Airport1, Airport2, MaxP, MinP, MaxD, MinD, no, CapWT, no, Solution) :-
    airport(Airport3, City, _), airport(Airport4, City, _),
    flight(Airport1, Airport3, CarrierNo13, FlightNo13, DepDate13, ArrDate13, Duration13, Price13),
    Flight1Info=f(Airport1, Airport3, CarrierNo13, FlightNo13, DepDate13, ArrDate13, Duration13, Price13),
    flight(Airport2, Airport4, CarrierNo23, FlightNo23, DepDate23, ArrDate23, Duration23, Price23),
    Flight2Info=f(Airport2, Airport4, CarrierNo23, FlightNo23, DepDate23, ArrDate23, Duration23, Price23),
    avg(Price13,Price23,AvgPrice),
    avg(Duration13,Duration23,AvgDuration),
    waitingTime(ArrDate13, DepDate23, WaitingTime), WaitingTime =< CapWT,
    travelScore(AvgPrice,AvgDuration,WaitingTime,MinP,MaxP,MinD,MaxD,CapWT,Rank),
    Solution=sol(AvgPrice, AvgDuration, WaitingTime, Rank, Flight1Info, Flight2Info).

eligibleFlights(Airport1, Airport2, MaxP, MinP, MaxD, MinD, yes, CapWT, yes, Solution) :-
    itinerary(Airport1, Airport3, OutboundFlight13, ReturnFlight13, Price13),
    itinerary(Airport2, Airport3, OutboundFlight23, ReturnFlight23, Price23),
    OutboundFlight13 = f(CarrierNo13, FlightNo13, DepDate13, ArrDate13, Duration13),
    OutboundFlight23 = f(CarrierNo23, FlightNo23, DepDate23, ArrDate23, Duration23),
    ReturnFlight13 = f(CarrierNo31, FlightNo31, DepDate31, ArrDate31, Duration31),
    ReturnFlight23 = f(CarrierNo32, FlightNo32, DepDate32, ArrDate32, Duration32),
    avg(Price13, Price23, AvgPrice),
    avg(Duration13, Duration23, AvgDuration),
    waitingTime(ArrDate13, DepDate23, WaitingTime), WaitingTime =< CapWT,
    travelScore(AvgPrice,AvgDuration,WaitingTime,MinP,MaxP,MinD,MaxD,CapWT,Rank),
    Flight1Info = f(Airport1, Airport3, CarrierNo13, FlightNo13, DepDate13, ArrDate13, Duration13, Price13),
    Flight1ReturnInfo = f(Airport3, Airport1, CarrierNo31, FlightNo31, DepDate31, ArrDate31, Duration31, Price13),
    Flight2Info = f(Airport2, Airport3, CarrierNo23, FlightNo23, DepDate23, ArrDate23, Duration23, Price23),
    Flight2ReturnInfo = f(Airport3, Airport2, CarrierNo32, FlightNo32, DepDate32, ArrDate32, Duration32, Price23),
    Solution=sol(AvgPrice, AvgDuration, WaitingTime, Rank, Flight1Info, Flight1ReturnInfo, Flight2Info, Flight2ReturnInfo).

eligibleFlights(Airport1, Airport2, MaxP, MinP, MaxD, MinD, yes, CapWT, no, Solution) :-
    airport(Airport3, City, _), airport(Airport4, City, _),
    itinerary(Airport1, Airport3, OutboundFlight13, ReturnFlight13, Price13),
    itinerary(Airport2, Airport4, OutboundFlight24, ReturnFlight24, Price24),
    OutboundFlight13 = f(CarrierNo13, FlightNo13, DepDate13, ArrDate13, Duration13),
    OutboundFlight24 = f(CarrierNo24, FlightNo24, DepDate24, ArrDate24, Duration24),
    ReturnFlight13 = f(CarrierNo31, FlightNo31, DepDate31, ArrDate31, Duration31),
    ReturnFlight24 = f(CarrierNo42, FlightNo42, DepDate42, ArrDate42, Duration42),
    avg(Price13, Price24, AvgPrice),
    avg(Duration13, Duration24, AvgDuration),
    waitingTime(ArrDate13, DepDate24, WaitingTime), WaitingTime =< CapWT,
    travelScore(AvgPrice,AvgDuration,WaitingTime,MinP,MaxP,MinD,MaxD,CapWT,Rank),
    Flight1Info = f(Airport1, Airport3, CarrierNo13, FlightNo13, DepDate13, ArrDate13, Duration13, Price13),
    Flight1ReturnInfo = f(Airport3, Airport1, CarrierNo31, FlightNo31, DepDate31, ArrDate31, Duration31, Price13),
    Flight2Info = f(Airport2, Airport4, CarrierNo24, FlightNo24, DepDate24, ArrDate24, Duration24, Price24),
    Flight2ReturnInfo = f(Airport4, Airport2, CarrierNo42, FlightNo42, DepDate42, ArrDate42, Duration42, Price24),
    Solution=sol(AvgPrice, AvgDuration, WaitingTime, Rank, Flight1Info, Flight1ReturnInfo, Flight2Info, Flight2ReturnInfo).

% normalize the values to get a travelScore between 0 - 1
travelScore(AvgPrice, AvgDuration, WaitingTime, MinP, MaxP, MinD, MaxD, CapWT, Rank) :-
    NormalizedPrice is (AvgPrice - MinP) / (MaxP - MinP),
    NormalizedDuration is (AvgDuration - MinD) / (MaxD - MinD),
    NormalizedWaitingTime is (WaitingTime) / (CapWT),
    wPrice(AP), wDuration(AD), wWaitingTime(AWT),
    Rank is AP*NormalizedPrice + AD*NormalizedDuration + AWT*NormalizedWaitingTime.

sortByStrategy(L, price, SortedL) :- sort(1, @=<, L, SortedL).
sortByStrategy(L, duration, SortedL) :- sort(2, @=<, L, SortedL).
sortByStrategy(L, waitingtime, SortedL) :- sort(3, @=<, L, SortedL).
sortByStrategy(L, bestsolution, SortedL) :- sort(4, @=<, L, SortedL).

% Predicate to find the max, min and avg of two numbers
max(A, B, Max) :- A >= B, Max is A.
max(A, B, Max) :- A < B, Max is B.

min(A, B, Min) :- A =< B, Min is A.
min(A, B, Min) :- A > B, Min is B.

avg(X,Y,A) :- A is (X+Y)/2.

% Predicate to find the maximum and minimum in a list of numbers
min_max_list([H|T], Min, Max) :- min_max_list(T, H, H, Min, Max).
min_max_list([], Min, Max, Min, Max).
min_max_list([H|T], CurrMin, CurrMax, Min, Max) :-
    min(H, CurrMin, NewMin), max(H, CurrMax, NewMax),
    min_max_list(T, NewMin, NewMax, Min, Max).

waitingTime(ArrDate13, DepDate23, WaitingTime) :-
    date_time_stamp(ArrDate13, ArrDate13ts),
    date_time_stamp(DepDate23, DepDate23ts),
    WaitingTime is abs(DepDate23ts - ArrDate13ts).

minAndMax(What, Return, Max, Min) :-
    getAll(What, Return, All),
    min_max_list(All, Min, Max).

getAll(price, no, Prices) :- findall(Price, flight(_, _, _, _, _, _, _, Price), Prices).
getAll(duration, no, Durations) :- findall(Duration, flight(_, _, _, _, _, _, Duration, _), Durations).

getAll(price, yes, Prices) :- findall(Price, itinerary(_, _, _, _, Price), Prices).
getAll(duration, yes, Durations) :- findall(Duration, itinerary(_, _, f(_,_,_,_,Duration), _, _), Durations).
