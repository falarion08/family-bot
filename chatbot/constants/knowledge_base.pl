
sibling(_,_) :- fail.
parent(_,_) :- fail.
child(_,_) :- fail.
male(_) :- fail.
female(_) :- fail.
sister(_,_) :- fail.
brother(_,_) :- fail.
mother(_,_) :- fail.
father(_,_) :- fail. 
grandmother(_,_) :- fail.
grandfather(_,_) :- fail.
uncle(_,_) :- fail.
aunt(_,_) :-fail.
daughter(_,_) :- fail.
son(_,_) :- fail.

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
:- discontiguous uncle/2.
:- discontiguous aunt/2.


are_siblings(X,Y) :- sibling(X,Y);sibling(Y,X);parent(_,Y), parent(_,X); child(X,_),child(Y,_);brother(X,Y);brother(Y,X);sister(X,Y);sister(Y,X).
is_sibling_title_assignable(SIBLING_TO_ASSIGN,X) :- are_siblings(X,X), \+ ( sister(SIBLING_TO_ASSIGN, X) ; brother(SIBLING_TO_ASSIGN, X) ).

is_parent_of(PARENT,CHILD) :- child(CHILD,PARENT); parent(PARENT,CHILD);father(PARENT,CHILD);mother(PARENT,CHILD).
is_parent_title_assignable(PARENT,CHILD) :- is_parent_of(PARENT,CHILD),\+ ( mother(PARENT, CHILD) ; father(PARENT, CHILD) ).

is_grandparent_of(GRANDPARENT,X) :- child(_,GRANDPARENT), parent(_,X);child(_,GRANDPARENT), parent(X,_);parent(GRANDPARENT,_), parent(_,X);parent(GRANDPARENT,_), parent(X,_).
is_grandparent_title_assignable(GRANDPARENT,X) :- is_grandparent_of(GRANDPARENT,X), \+ ( grandmother(GRANDPARENT, X) ; father(GRANDPARENT, X) ).

is_child_of(CHILD,PARENT) :- child(CHILD,PARENT);is_parent_of(PARENT,CHILD);son(CHILD,PARENT);daughter(CHILD,PARENT).
is_child_title_assignable(CHILD,PARENT) :- is_child_of(CHILD,PARENT), \+ (daughter(CHILD,PARENT);son(CHILD,PARENT)).

is_aunt_title_assignable(PIBLING, X) :-
    are_siblings(PIBLING, _),
    ( child(X, _) ; is_parent_of(_, X) ),
    ( sister(PIBLING, _) ; \+ uncle(PIBLING,X) ).

is_uncle_title_assignable(PIBLING, X) :-
    are_siblings(PIBLING, _),
    ( child(X, _) ; is_parent_of(_, X) ),
    ( brother(PIBLING, _) ; \+ aunt(PIBLING,X) ).

father(one,two).
father(two,three).
