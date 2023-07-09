/* 
TODO:
    - convert data into prolog facts 
    - consider city as destination, not airport (allow the user to set a "sameAirport" flag)
    - handle data conversion from/to date to/from timestamp (check how to handle time zones)
    - specify one-way or return flight, and specify departure and return dates
    - specify max price, max duration, max waiting time
    - specify TargetCities or TargetCountries 
    - find a way to evaluate return solutions (e.g. if the return flight is too expensive, the solution is not good)
    - include proximity airports
*/

% airport(AirportId).
airport(fra). % Frankfurt: partenza1
    in(fra, de). % Germany
    city(fra, frankfurt).
airport(ory).
    in(ory, fr). % France
    city(ory, paris).
airport(cdg).
    in(cdg, fr). % France
    city(cdg, paris). 
airport(psa). % Pisa: partenza2
    in(psa, it). % Italy
    city(psa, pisa).
airport(lis).
    in(lis, pt). % Portugal
    city(lis, lisbon).
airport(vce).
    in(vce, it). % Italy
    city(vce, venice).

% flight(Origin, Destination, CarrierNo, FlightNo, DepDate, ArrDate, Duration, Price).
% TODO: handle dates in the format 'date(Y,M,D,H,Mn,S,Off,TZ,DST)'
%       https://www.swi-prolog.org/pldoc/man?section=timedate
flight(fra, ory, lh, 1234, 10, 11, 1, 100).
flight(fra, ory, lh, 1234, 11, 12, 1, 12).
flight(fra, cdg, af, 1234, 10, 11, 1, 20).
flight(psa, ory, fr, 4567, 9, 11, 2, 30).
flight(fra, lis, lh, 1234, 12, 16, 4, 40).
flight(psa, lis, lh, 2345, 11, 15, 4, 50).

% SortStrategy \in {price, duration, waitingtime, bestsolution}
fly2Meet(Airport1, Airport2, SortStrategy, Flights) :-
    airport(Airport1), airport(Airport2), dif(Airport1, Airport2),
    findall(FCombo, findFlights(Airport1, Airport2, FCombo), TmpFlights),
    sortByStrategy(TmpFlights, SortStrategy, Flights).

%  Flight1Info, Flight2Info, AvgPrice, AvgDuration, WaitingTime
findFlights(Airport1, Airport2, sol(AvgPrice, AvgDuration, WaitingTime, Rank, Flight1Info, Flight2Info)) :-
    flight(Airport1, Airport3, CarrierNo13, FlightNo13, DepDate13, ArrDate13, Duration13, Price13),
    flight(Airport2, Airport3, CarrierNo23, FlightNo23, DepDate23, ArrDate23, Duration23, Price23),
    AvgPrice is (Price13 + Price23) / 2,
    AvgDuration is (Duration13 + Duration23) / 2,
    WaitingTime is abs(ArrDate13 - ArrDate23),
    Rank is AvgPrice + AvgDuration + WaitingTime, % TODO: normalise values, consider if same airport
    Flight1Info = f(Airport1, Airport3, CarrierNo13, FlightNo13, DepDate13, ArrDate13, Duration13, Price13),
    Flight2Info = f(Airport2, Airport3, CarrierNo23, FlightNo23, DepDate23, ArrDate23, Duration23, Price23).

sortByStrategy(L, price, SortedL) :- sort(L, SortedL).
sortByStrategy(L, duration, SortedL) :- sort(2, @=<, L, SortedL).
sortByStrategy(L, waitingtime, SortedL) :- sort(3, @=<, L, SortedL).
sortByStrategy(L, bestsolution, SortedL) :- sort(4, @=<, L, SortedL).



