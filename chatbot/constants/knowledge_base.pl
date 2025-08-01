
sibling(_,_) :- fail.
parent(_,_) :- fail.
child(_,_) :- fail.
male(_) :- fail.
female(_) :- fail.

:- discontiguous sibling/2.
:- discontiguous parent/2.
:- discontiguous child/2.
:- discontiguous male/1.
:- discontiguous female/1.
:- discontiguous sister/2.
:- discontiguous brother/2.
:- discontiguous mother/2.
:- discontiguous father/2.
:- discontiguous grandmother/2.
:- discontiguous grandfather/2.


sister(SIBLING,X) :- sibling(SIBLING,X), \+ male(SIBLING); sibling(X,SIBLING),\+ male(SIBLING); parent(_,SIBLING), parent(_,X), female(SIBLING).
brother(SIBLING,X) :- sibling(SIBLING,X), \+ female(SIBLING); sibling(X,SIBLING),\+ female(SIBLING); parent(_,SIBLING), parent(_,X), female(SIBLING). 

mother(PARENT,CHILD) :- child(CHILD,PARENT), \+ male(PARENT); parent(PARENT,CHILD), \+ male(PARENT).
father(PARENT,CHILD) :- child(CHILD,PARENT), \+ female(PARENT); parent(PARENT,CHILD), \+ female(PARENT).

grandmother(GRANDPARENT,X) :- child(_,GRANDPARENT), parent(_,X), \+ male(GRANDPARENT);child(_,GRANDPARENT), parent(X,_), \+ male(GRANDPARENT);parent(GRANDPARENT,_), parent(_,X), \+ male(GRANDPARENT);parent(GRANDPARENT,_), parent(X,_), \+ male(GRANDPARENT).
grandfather(GRANDPARENT,X) :- child(_,GRANDPARENT), parent(_,X), \+ female(GRANDPARENT);child(_,GRANDPARENT), parent(X,_), \+ female(GRANDPARENT);parent(GRANDPARENT,_), parent(_,X), \+ female(GRANDPARENT);parent(GRANDPARENT,_), parent(X,_), \+ female(GRANDPARENT).
                   