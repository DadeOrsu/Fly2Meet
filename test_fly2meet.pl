% TODO: aggiungere tests per voli con ritorno e raffinare i test esistenti.
% TODO: guardare come fare cleanup tra un test e altro. Ogni test deve essere indipendente dagli altri.

:- begin_tests(fly2meet).

:- dynamic(airport/3).
:- dynamic(flight/8).
:- dynamic(itinerary/5).

setup1 :-
    consult('prologFacts/test1.pl').

setup2 :-
    consult('prologFacts/test2.pl').

teardown1 :-
    retractall(airport(_, _, _)),
    retractall(flight(_, _, _, _, _, _, _, _)).

teardown2 :-
    retractall(airport(_, _, _)),
    retractall(itinerary(_, _, _, _, _)).

test(fly2meet_case1, [setup(setup1), cleanup(teardown1)]) :-
    consult(fly2meet),
    fly2meet(cdg, lhr, bestsolution, no, 4000, yes, yes, Flights),
    assertion(nonvar(Flights)).

test(fly2meet_case2, [setup(setup1), cleanup(teardown1)]) :-
    consult(fly2meet),
    fly2meet(cdg, lhr, bestsolution, no, 4000, yes, no, Flights),
    assertion(nonvar(Flights)).

test(fly2meet_case3, [setup(setup1), cleanup(teardown1)]) :-
    consult(fly2meet),
    fly2meet(cdg, lhr, bestsolution, no, 4000, no, yes, Flights),
    assertion(nonvar(Flights)).

test(fly2meet_case4, [setup(setup1), cleanup(teardown1)]) :-
    consult(fly2meet),
    fly2meet(cdg, lhr, bestsolution, no, 4000, no, no, Flights),
    assertion(nonvar(Flights)).

test(fly2meet_case5, [setup(setup2), cleanup(teardown2)]) :-
    consult(fly2meet),
    fly2meet(cdg, lhr, bestsolution, yes, 4000, yes, yes, Flights),
    assertion(nonvar(Flights)).

test(fly2meet_case6, [setup(setup2), cleanup(teardown2)]) :-
    consult(fly2meet),
    fly2meet(cdg, lhr, bestsolution, yes, 4000, yes, no, Flights),
    assertion(nonvar(Flights)).

test(fly2meet_case7, [setup(setup2), cleanup(teardown2)]) :-
    consult(fly2meet),
    fly2meet(cdg, lhr, bestsolution, yes, 4000, no, yes, Flights),
    assertion(nonvar(Flights)).

test(fly2meet_case8, [setup(setup2), cleanup(teardown2)]) :-
    consult(fly2meet),
    fly2meet(cdg, lhr, bestsolution, yes, 4000, no, no, Flights),
    assertion(nonvar(Flights)).
:- end_tests(fly2meet).

