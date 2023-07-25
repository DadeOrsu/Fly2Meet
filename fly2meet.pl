:- discontiguous airport/1.
:- discontiguous in/2.
:- discontiguous city/2.
:- consult('prologFacts/prolog_facts.pl').

fly2meet(Airport1, Airport2, SortStrategy, Flights) :-
    airport(Airport1), airport(Airport2), dif(Airport1, Airport2),
    % find max and min flight price, duration, and waiting time
    find_max_and_min_flight_price(MaxPrice, MinPrice),
    find_max_and_min_flight_duration(MaxDuration, MinDuration),
    find_max_and_min_waiting_time(MaxWaitingTime, MinWaitingTime),
    % find all possible flights
    findall(FCombo, findFlights(Airport1, Airport2, MaxPrice, MinPrice, MaxDuration, MinDuration, MaxWaitingTime, MinWaitingTime, FCombo), TmpFlights),
    sortByStrategy(TmpFlights, SortStrategy, Flights).

findFlights(Airport1, Airport2, MaxPrice, MinPrice, MaxDuration, MinDuration, MaxWaitingTime, MinWaitingTime, sol(AvgPrice, AvgDuration, WaitingTime, Rank, Flight1Info, Flight2Info)) :-
    flight(Airport1, Airport3, CarrierNo13, FlightNo13, DepDate13, ArrDate13, Duration13, Price13),
    flight(Airport2, Airport3, CarrierNo23, FlightNo23, DepDate23, ArrDate23, Duration23, Price23),
    AvgPrice is (Price13 + Price23) / 2,
    AvgDuration is (Duration13 + Duration23) / 2,
    get_waiting_time(ArrDate13, DepDate23, WaitingTime),
    % normalize the values to get a score between 0 - 1
    NormalizedPrice is (AvgPrice - MinPrice) / (MaxPrice - MinPrice),
    NormalizedDuration is (AvgDuration - MinDuration) / (MaxDuration - MinDuration),
    NormalizedWaitingTime is (WaitingTime - MinWaitingTime) / (MaxWaitingTime - MinWaitingTime),
    % calculate the rank as the sum of the normalized values
    Rank is NormalizedPrice + NormalizedDuration + NormalizedWaitingTime,
    Flight1Info = f(Airport1, Airport3, CarrierNo13, FlightNo13, DepDate13, ArrDate13, Duration13, Price13),
    Flight2Info = f(Airport2, Airport3, CarrierNo23, FlightNo23, DepDate23, ArrDate23, Duration23, Price23).

sortByStrategy(L, price, SortedL) :- sort(1, @=<, L, SortedL).
sortByStrategy(L, duration, SortedL) :- sort(2, @=<, L, SortedL).
sortByStrategy(L, waitingtime, SortedL) :- sort(3, @=<, L, SortedL).
sortByStrategy(L, bestsolution, SortedL) :- sort(4, @=<, L, SortedL).

% Predicate to find the minimum of two numbers
min(A, B, Min) :- A =< B, Min is A.
min(A, B, Min) :- A > B, Min is B.

% Predicate to find the maximum of two numbers
max(A, B, Max) :- A >= B, Max is A.
max(A, B, Max) :- A < B, Max is B.

% Predicate to find the maximum and minimum in a list of numbers
min_max_list([H|T], Min, Max) :- min_max_list(T, H, H, Min, Max).
min_max_list([], Min, Max, Min, Max).
min_max_list([H|T], CurrMin, CurrMax, Min, Max) :-
    min(H, CurrMin, NewMin),
    max(H, CurrMax, NewMax),
    min_max_list(T, NewMin, NewMax, Min, Max).

% Predicate to get the waiting time between two date_time_stamp
get_waiting_time(ArrDate13, DepDate23, WaitingTime) :-
    date_time_stamp(ArrDate13, ArrDate13ts),
    date_time_stamp(DepDate23, DepDate23ts),
    WaitingTime is abs(DepDate23ts - ArrDate13ts).

% Predicate to get all flight prices
get_all_prices(Prices) :-
    findall(Price, flight(_, _, _, _, _, _, _, Price), Prices).

% Predicate to get all flight durations
get_all_durations(Durations) :-
    findall(Duration, flight(_, _, _, _, _, _, Duration, _), Durations).

% Predicate to get all the wait times between two flights
get_all_waiting_times(WaitingTimes) :-
    findall(WaitingTime, (flight(_, _, _, _, _, ArrDate1, _, _), flight(_, _, _, _, DepDate2, _, _, _), get_waiting_time(ArrDate1, DepDate2, WaitingTime)), WaitingTimes).

% Predicate to call to get the highest and lowest price among all available flights
find_max_and_min_flight_price(MaxPrice, MinPrice) :-
    get_all_prices(Prices),
    min_max_list(Prices, MinPrice, MaxPrice).

% Predicate to get the maximum and minimum duration among all available flights
find_max_and_min_flight_duration(MaxDuration, MinDuration) :-
    get_all_durations(Durations),
    min_max_list(Durations, MinDuration, MaxDuration).

% Predicate to get the maximum and minimum wait time among all available flights
find_max_and_min_waiting_time(MaxWaitingTime, MinWaitingTime) :-
    get_all_waiting_times(WaitingTimes),
    min_max_list(WaitingTimes, MinWaitingTime, MaxWaitingTime).
