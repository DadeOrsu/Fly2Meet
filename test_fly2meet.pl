% TODO: aggiungere tests per voli con ritorno e raffinare i test esistenti.
% TODO: guardare come fare cleanup tra un test e altro. Ogni test deve essere indipendente dagli altri.

:- begin_tests(fly2meet).

:- consult(fly2meet).
:- consult('prologFacts/prolog_facts.pl').

test(fly2meet_case1) :-
    fly2meet(cdg, lhr, bestsolution, no, 4000, yes, yes, Flights),
    assertion(nonvar(Flights)).

test(fly2meet_case2) :-
    fly2meet(cdg, lhr, bestsolution, no, 4000, yes, no, Flights),
    assertion(nonvar(Flights)).

test(fly2meet_case3) :-
    fly2meet(cdg, lhr, bestsolution, no, 4000, no, yes, Flights),
    assertion(nonvar(Flights)).

test(fly2meet_case4) :-
    fly2meet(cdg, lhr, bestsolution, no, 4000, no, no, Flights),
    assertion(nonvar(Flights)).

:- end_tests(fly2meet).

