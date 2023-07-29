:- discontiguous airport/1.
:- discontiguous in/2.
:- discontiguous city/2.
:- consult('prologFacts/prolog_facts.pl').

% TODO:
% 1. aggiungere flag SameAirport, p.e. estendendo la rappresentazione da airport(Code) a airport(Code, City, Country).
% 2. explicitly represent and handle itineraries in eligibleFlights with yes... p.e.
    % - itinerary(Airport1, Airport2, OutboundFlight12, ReturnFlight12, Price), % f(CarrierNo13, FlightNo13, DepDate13, ArrDate13)
    % - flight(Airport1, Airport3, CarrierNo13, FlightNo13, DepDate13, ArrDate13, Duration13, Price13)

wPrice(AP) :- AP is 1/3.
wDuration(AD) :- AD is 1/3.
wWaitingTime(AWT) :- AWT is 1/3.

fly2meet(Airport1, Airport2, SortStrategy, Return, Flights) :-
    fly2meet(Airport1, Airport2, SortStrategy, Return, inf, Flights).

fly2meet(Airport1, Airport2, SortStrategy, Return, CapWT, Flights) :-
    airport(Airport1), airport(Airport2), dif(Airport1, Airport2),
    minAndMax(price,MaxP, MinP),
    minAndMax(duration,MaxD, MinD),
    minAndMax(waitingtimes,MaxWT, MinWT),
    setof(FCombo, eligibleFlights(Airport1, Airport2, MaxP, MinP, MaxD, MinD, MaxWT, MinWT, Return, CapWT, FCombo), TmpFlights),
    sortByStrategy(TmpFlights, SortStrategy, Flights).

eligibleFlights(Airport1, Airport2, MaxP, MinP, MaxD, MinD, MaxWT, MinWT, no, CapWT, Solution) :-
    flight(Airport1, Airport3, CarrierNo13, FlightNo13, DepDate13, ArrDate13, Duration13, Price13),
    Flight1Info=f(Airport1, Airport3, CarrierNo13, FlightNo13, DepDate13, ArrDate13, Duration13, Price13),
    flight(Airport2, Airport3, CarrierNo23, FlightNo23, DepDate23, ArrDate23, Duration23, Price23),
    Flight2Info=f(Airport2, Airport3, CarrierNo23, FlightNo23, DepDate23, ArrDate23, Duration23, Price23),
    avg(Price13,Price23,AvgPrice),
    avg(Duration13,Duration23,AvgDuration),
    waitingTime(ArrDate13, DepDate23, WaitingTime), WaitingTime =< CapWT,
    travelScore(AvgPrice,AvgDuration,WaitingTime,MinP,MaxP,MinD,MaxD,MinWT,MaxWT,Rank),
    Solution=sol(AvgPrice, AvgDuration, WaitingTime, Rank, Flight1Info, Flight2Info).



eligibleFlights(Airport1, Airport2, MaxP, MinP, MaxD, MinD, MaxWT, MinWT, yes, CapWT, Solution) :-
    flight(Airport1, Airport3, CarrierNo13, FlightNo13, DepDate13, ArrDate13, Duration13, Price13),
    Flight1Info=f(Airport1, Airport3, CarrierNo13, FlightNo13, DepDate13, ArrDate13, Duration13, Price13),
    flight(Airport2, Airport3, CarrierNo23, FlightNo23, DepDate23, ArrDate23, Duration23, Price23),
    Flight2Info=f(Airport2, Airport3, CarrierNo23, FlightNo23, DepDate23, ArrDate23, Duration23, Price23),
    avg(Price13, Price23, AvgPrice),
    avg(Duration13, Duration23, AvgDuration),
    waitingTime(ArrDate13, DepDate23, WaitingTime), WaitingTime =< CapWT,
    travelScore(AvgPrice,AvgDuration,WaitingTime,MinP,MaxP,MinD,MaxD,MinWT,MaxWT,Rank),
    Flight1Info = f(Airport1, Airport3, CarrierNo13, FlightNo13, DepDate13, ArrDate13, Duration13, Price13),
    Flight1ReturnInfo = f(Airport3, Airport1, CarrierNo31, FlightNo31, DepDate31, ArrDate31, Duration31, Price13),
    flight(Airport3, Airport1, CarrierNo31, FlightNo31, DepDate31, ArrDate31, Duration31, Price13),
    Flight2Info = f(Airport2, Airport3, CarrierNo23, FlightNo23, DepDate23, ArrDate23, Duration23, Price23),
    Flight2ReturnInfo = f(Airport3, Airport2, CarrierNo32, FlightNo32, DepDate32, ArrDate32, Duration32, Price23),
    flight(Airport3, Airport2, CarrierNo32, FlightNo32, DepDate32, ArrDate32, Duration32, Price23),
    Solution=sol(AvgPrice, AvgDuration, WaitingTime, Rank, Flight1Info, Flight1ReturnInfo, Flight2Info, Flight2ReturnInfo).

% normalize the values to get a travelScore between 0 - 1
travelScore(AvgPrice, AvgDuration, WaitingTime, MinP, MaxP, MinD, MaxD, MinWT, MaxWT, Rank) :-
    NormalizedPrice is (AvgPrice - MinP) / (MaxP - MinP),
    NormalizedDuration is (AvgDuration - MinD) / (MaxD - MinD),
    NormalizedWaitingTime is (WaitingTime - MinWT) / (MaxWT - MinWT),
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

minAndMax(What, Max, Min) :-
    getAll(What,All),
    min_max_list(All, Min, Max).

getAll(price, Prices) :- findall(Price, flight(_, _, _, _, _, _, _, Price), Prices).
getAll(duration, Durations) :- findall(Duration, flight(_, _, _, _, _, _, Duration, _), Durations).
getAll(waitingtimes, WaitingTimes) :- findall(WaitingTime, (flight(_, _, _, _, _, ArrDate1, _, _), flight(_, _, _, _, DepDate2, _, _, _), waitingTime(ArrDate1, DepDate2, WaitingTime)), WaitingTimes).
