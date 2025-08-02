
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
:- discontiguous son/2.
:- discontiguous daughter/2.
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


is_sibling_of(X,Y) :- 
     sibling(X,Y);
     sibling(Y,X);
     parent(_,Y), parent(_,X);
     mother(_,Y), mother(_,X); 
     father(_,Y), father(_,X);  
     child(X,_),child(Y,_);
     brother(X,Y);
     brother(Y,X);
     sister(X,Y);
     sister(Y,X).

is_sibling_title_assignable(SIBLING_TO_ASSIGN,X) :- is_sibling_of(SIBLING_TO_ASSIGN,X), \+ ( sister(SIBLING_TO_ASSIGN, X) ; brother(SIBLING_TO_ASSIGN, X) ).

is_sister_of(X,Y) :- 
     sister(X,Y);
     sister(X,_), is_sibling_of(_,Y), is_parent_of(_,X),is_parent_of(_,Y).

is_brother_of(X,Y) :-
     brother(X,Y);
     brother(X,_), is_sibling_of(_,Y), is_parent_of(_,X),is_parent_of(_,Y).

is_parent_of(PARENT,CHILD) :- 
     child(CHILD,PARENT);
     son(CHILD,PARENT);
     daughter(CHILD,PARENT);
     ( child(_,PARENT);son(_,PARENT);daughter(_,PARENT) ), is_sibling_of(_,CHILD);
     parent(PARENT,CHILD);
     father(PARENT,CHILD);
     mother(PARENT,CHILD);
     ( parent(PARENT,_),mother(PARENT,_);father(PARENT,_) ), is_sibling_of(_,CHILD).

is_parent_title_assignable(PARENT,CHILD) :- is_parent_of(PARENT,CHILD),\+ ( mother(PARENT, CHILD) ; father(PARENT, CHILD) ).

is_grandparent_of(GRANDPARENT,X) :- 
     (child(_,GRANDPARENT);son(_,GRANDPARENT);daughter(_,GRANDPARENT)), ( parent(_,X), father(_,X) ; mother(_, X);child(X,_);son(X,_);daughter(X,_) );
     (parent(GRANDPARENT,_);mother(GRANDPARENT,_);father(GRANDPARENT,_) ), ( parent(_,X), father(_,X) ; mother(_, X);child(X,_);son(X,_);daughter(X,_) ).

is_grandparent_title_assignable(GRANDPARENT,X) :- is_grandparent_of(GRANDPARENT,X), \+ ( grandmother(GRANDPARENT, X) ; grandfather(GRANDPARENT, X) ).

is_grandmother_of(GRANDPARENT,X) :- 
     father(GRANDPARENT,_), ( parent(_,X), father(_,X) ; mother(_, X) );
     father(GRANDPARENT,_), ( child(X,_);son(X,_);daughter(X,_) ).

is_grandmother_of(GRANDPARENT,X) :- 
     father(GRANDPARENT,_), is_parent_of(_,X);
     father(GRANDPARENT,_), is_child_of(X,_).


is_child_of(CHILD,PARENT) :- 
     child(CHILD,PARENT);
     daughter(CHILD,PARENT);
     son(CHILD,PARENT);
     child(_,PARENT),(
          sibling(CHILD,_);sibling(_,CHILD);sister(CHILD,_);sister(_,CHILD);brother(CHILD,_);brother(_,CHILD));
     parent(PARENT,_),(
          sibling(CHILD,_);sibling(_,CHILD);sister(CHILD,_);sister(_,CHILD);brother(CHILD,_);brother(_,CHILD)).

is_child_title_assignable(CHILD,PARENT) :- is_child_of(CHILD,PARENT), \+ (daughter(CHILD,PARENT);son(CHILD,PARENT)).

is_daughter_of(CHILD,PARENT) :- 
     daughter(CHILD,PARENT),
     sister(CHILD,_), ( child(_,PARENT);son(_,PARENT);daughter(_,PARENT) );
     sister(CHILD,_), ( parent(PARENT,_);daughter(PARENT,_);son(PARENT,_) ).

is_son_of(CHILD,PARENT) :- 
     son(CHILD,PARENT), 
     brother(CHILD,_), ( child(_,PARENT);son(_,PARENT);daughter(_,PARENT) );
     brother(CHILD,_), ( parent(PARENT,_);daughter(PARENT,_);son(PARENT,_) ).


is_aunt_title_assignable(PIBLING, X) :-
    is_sibling_of(PIBLING, _),
    ( is_child_of(X, _) ; is_parent_of(_, X) ),
    ( sister(PIBLING, _) ; \+ uncle(PIBLING,X) ).

is_uncle_title_assignable(PIBLING, X) :-
     uncle(PIBLING,X);
     sister(PIBLING,_), is_sibling_of(PIBLING, _),
     ( is_child_of(X, _) ; is_parent_of(_, X) ).

is_aunt_of(PIBLING,X) :-
     aunt(PIBLING,X);
     sister(PIBLING,_), is_sibling_of(PIBLING, _),
     ( is_child_of(X, _) ; is_parent_of(_, X) ).
brother(sigma,ph).
son(viet,ph).
aunt(sigma,viet).
