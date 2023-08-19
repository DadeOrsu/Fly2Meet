:- consult(fly2meet).

:- consult('prologFacts/prolog_facts.pl').

:- begin_tests(fly2meet).

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

