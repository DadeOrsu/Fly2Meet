% TODO: aggiungere tests per voli con ritorno e raffinare i test esistenti.
% TODO: guardare come fare cleanup tra un test e altro. Ogni test deve essere indipendente dagli altri.

:- begin_tests(fly2meet).

:- dynamic(airport/3).
:- dynamic(flight/8).
setup :-
    consult('prologFacts/prolog_facts.pl').

teardown :-
    retractall(airport(_, _, _)),
    retractall(flight(_, _, _, _, _, _, _, _)).

:- consult(fly2meet).

test(fly2meet_case1, [setup(setup), cleanup(teardown)]) :-
    fly2meet(cdg, lhr, bestsolution, no, 4000, yes, yes, Flights),
    assertion(nonvar(Flights)).

test(fly2meet_case2, [setup(setup), cleanup(teardown)]) :-
    fly2meet(cdg, lhr, bestsolution, no, 4000, yes, no, Flights),
    assertion(nonvar(Flights)).

test(fly2meet_case3, [setup(setup), cleanup(teardown)]) :-
    fly2meet(cdg, lhr, bestsolution, no, 4000, no, yes, Flights),
    assertion(nonvar(Flights)).

test(fly2meet_case4, [setup(setup), cleanup(teardown)]) :-
    fly2meet(cdg, lhr, bestsolution, no, 4000, no, no, Flights),
    assertion(nonvar(Flights)).

:- end_tests(fly2meet).

