:- consult('prologFacts/prolog_facts.pl').

fly2Meet(Airport1, Airport2, SortStrategy, Flights) :-
    airport(Airport1), airport(Airport2), dif(Airport1, Airport2),
    % find max price, duration, waiting time
    find_max_flight_price(MaxPrice),
    find_max_flight_duration(MaxDuration),
    find_max_waiting_time(MaxWaitingTime),
    % find all possible flights
    findall(FCombo, findFlights(Airport1, Airport2, MaxPrice, MaxDuration, MaxWaitingTime, FCombo), TmpFlights),
    sortByStrategy(TmpFlights, SortStrategy, Flights),
    printFlights(Flights).

printFlights([]).
printFlights([sol(_, _, _, _, Flight1Info, Flight2Info)|Rest]) :-
    format("Flight 1: ~w~n", [Flight1Info]),
    format("Flight 2: ~w~n", [Flight2Info]),
    printFlights(Rest).

findFlights(Airport1, Airport2, MaxPrice, MaxDuration, MaxWaitingTime, sol(AvgPrice, AvgDuration, WaitingTime, Rank, Flight1Info, Flight2Info)) :-
    flight(Airport1, Airport3, CarrierNo13, FlightNo13, DepDate13, ArrDate13, Duration13, Price13),
    flight(Airport2, Airport3, CarrierNo23, FlightNo23, DepDate23, ArrDate23, Duration23, Price23),
    AvgPrice is (Price13 + Price23) / 2,
    AvgDuration is (Duration13 + Duration23) / 2,
    date_time_stamp(ArrDate13, ArrDate13ts),
    date_time_stamp(ArrDate23, ArrDate23ts),
    WaitingTime is abs(ArrDate23ts - ArrDate13ts),
    % I normalize the values to get a score between 0 - 1
    NormalizedPrice is (Price13 + Price23) / (2 * MaxPrice),
    NormalizedDuration is (Duration13 + Duration23) / (2 * MaxDuration),
    NormalizedWaitingTime is WaitingTime / MaxWaitingTime,
    % I calculate the rank as the sum of the normalized values
    Rank is NormalizedPrice + NormalizedDuration + NormalizedWaitingTime,
    Flight1Info = f(Airport1, Airport3, CarrierNo13, FlightNo13, DepDate13, ArrDate13, Duration13, Price13),
    Flight2Info = f(Airport2, Airport3, CarrierNo23, FlightNo23, DepDate23, ArrDate23, Duration23, Price23).


sortByStrategy(L, price, SortedL) :- sort(1, @=<, L, SortedL).
sortByStrategy(L, duration, SortedL) :- sort(2, @=<, L, SortedL).
sortByStrategy(L, waitingtime, SortedL) :- sort(3, @=<, L, SortedL).
sortByStrategy(L, bestsolution, SortedL) :- sort(4, @=<, L, SortedL).



% Predicate to find the maximum of two numbers
max(A, B, Max) :- A >= B, Max is A.
max(A, B, Max) :- A < B, Max is B.

% Predicate to find the maximum in a list of numbers
max_list([], 0).  % Ritorna 0 se la lista è vuota (nessun volo)
max_list([H | T], MaxPrice) :-
    max_list(T, RestMax),
    max(H, RestMax, MaxPrice).

% Predicate to get the price of a flight
get_price(flight(_, _, _, _, _, _, _, Price), Price).

% Predicate to get all flight prices
get_all_prices(Prices) :-
    findall(Price, flight(_, _, _, _, _, _, _, Price), Prices).

% Predicate to call to get the highest price among all available flights
find_max_flight_price(MaxPrice) :-
    get_all_prices(Prices),
    max_list(Prices, MaxPrice).

% Predicate to get all flight durations
get_all_durations(Durations) :-
    findall(Duration, flight(_, _, _, _, _, _, Duration, _), Durations).

% Predicate to get the maximum duration among all available flights
find_max_flight_duration(MaxDuration) :-
    get_all_durations(Durations),
    max_list(Durations, MaxDuration).

% Predicate to get the waiting time between two flights
get_waiting_time(flight(_, _, _, _, _, ArrDate1, _, _), flight(_, _, _, _, DepDate2, _, _, _), WaitingTime) :-
    date_time_stamp(ArrDate1, ArrDate1ts),
    date_time_stamp(DepDate2, DepDate2ts),
    WaitingTime is abs(DepDate2ts - ArrDate1ts).

% Predicate to get all the wait times between two flights
get_all_waiting_times(WaitingTimes) :-
    findall(WaitingTime, (flight(_, _, _, _, _, ArrDate1, _, _), flight(_, _, _, _, DepDate2, _, _, _), get_waiting_time(flight(_, _, _, _, _, ArrDate1, _, _), flight(_, _, _, _, DepDate2, _, _, _), WaitingTime)), WaitingTimes).

% Predicate to get the maximum wait time among all available flights
find_max_waiting_time(MaxWaitingTime) :-
    get_all_waiting_times(WaitingTimes),
    max_list(WaitingTimes, MaxWaitingTime).