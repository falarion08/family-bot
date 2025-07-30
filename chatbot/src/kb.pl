male(_) :- fail.
female(_) :- fail.
sibling(_,_):-fail.
sister(_,_):-fail.
brother(_,_):-fail.
child(_,_):-fail.
daughter(_,_):-fail.
son(_,_):-fail.
father(_,_):-fail.
mother(_,_):-fail.
grandfather(_,_):-fail.
grandmother(_,_):-fail.
parent(_,_) :-fail.

parent(martin, annie).
parent(martin, unnie).

sibling(r,s).

sibling(X, Y) :-
    parent(Z, X),
    parent(Z, Y).

sibling(X,Y):-sibling(Y,Z), X = Z,!.
