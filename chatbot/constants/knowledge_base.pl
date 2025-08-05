
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

     parent(P,Y), parent(P,X);
     mother(P,Y), mother(P,X); 
     father(P,Y), father(P,X);
     
     parent(P,Y), child(X,P);
     mother(M,Y), daughter(X,M); 
     father(F,Y), son(F,X);

     ( child(X,PLACEHOLDER);son(X,PLACEHOLDER);daughter(X,PLACEHOLDER) ) , ( child(Y,PLACEHOLDER);son(Y,PLACEHOLDER);daughter(Y,PLACEHOLDER);parent(PLACEHOLDER,Y);mother(PLACEHOLDER,Y);father(PLACEHOLDER,Y) );
     ( parent(PLACEHOLDER,X);mother(PLACEHOLDER,X);father(PLACEHOLDER,X)) , ( child(Y,PLACEHOLDER);son(Y,PLACEHOLDER);daughter(Y,PLACEHOLDER);parent(PLACEHOLDER,Y);mother(PLACEHOLDER,Y);father(PLACEHOLDER,Y) );

     brother(X,Y);
     brother(Y,X);
     sister(X,Y);
     sister(Y,X).


is_sibling_title_assignable(SIBLING_TO_ASSIGN,X) :-
     is_sibling_of(SIBLING_TO_ASSIGN,X).

is_sister_title_assignable(SIBLING_TO_ASSIGN,X) :- 
     is_sibling_of(SIBLING_TO_ASSIGN,X), 
     \+ ( sister(SIBLING_TO_ASSIGN, X) ; brother(SIBLING_TO_ASSIGN, X) ),
     \+ has_male_title(SIBLING_TO_ASSIGN).

is_brother_title_assignable(SIBLING_TO_ASSIGN,X) :- 
     is_sibling_of(SIBLING_TO_ASSIGN,X), 
     \+ ( sister(SIBLING_TO_ASSIGN, X) ; brother(SIBLING_TO_ASSIGN, X) ),
     \+ has_female_title(SIBLING_TO_ASSIGN).

is_sister_of(X,Y) :- 
     sister(X,Y);
     sister(X,Z), is_sibling_of(Z,Y), is_parent_of(Z,X),is_parent_of(Z,Y);
     aunt(X,Z), ( child(Z,Y);daughter(Z,Y);son(Z,Y) );
     aunt(X,Z), ( parent(Y,Z);mother(Y,Z);father(Y,Z) ).


is_brother_of(X,Y) :-
     brother(X,Y);
     brother(X,Z), is_sibling_of(Z,Y), is_parent_of(Z,X),is_parent_of(Z,Y);
     uncle(X,Z), ( child(Z,Y);daughter(Z,Y);son(Z,Y) );
     uncle(X,Z), ( parent(Y,Z);mother(Y,Z);father(Y,Z) ).


is_parent_of(PARENT,CHILD) :- 
     child(CHILD,PARENT);
     son(CHILD,PARENT);
     daughter(CHILD,PARENT);
     ( parent(PARENT,X);mother(PARENT,X);father(PARENT,X) ), (sibling(X,CHILD);sibling(CHILD,X);sister(X,CHILD);sister(CHILD,X);brother(X,CHILD);brother(CHILD,X) );
     ( child(X,PARENT);son(X,PARENT);daughter(X,PARENT) ), (sibling(X,CHILD);sibling(CHILD,X);sister(X,CHILD);sister(CHILD,X);brother(X,CHILD);brother(CHILD,X) );
     parent(PARENT,CHILD);
     father(PARENT,CHILD);
     mother(PARENT,CHILD).

is_parent_title_assignable(PARENT,CHILD) :- 
     is_parent_of(PARENT,CHILD). 

is_mother_of(PARENT,CHILD):-
     mother(PARENT,CHILD);
     mother(PARENT, X ), (sibling(CHILD,X);sibling(X,CHILD);sister(CHILD,X);sister(X,CHILD);brother(CHILD,X);brother(X,CHILD)).

is_father_of(PARENT,CHILD):-
     father(PARENT,CHILD);
     father(PARENT, X ), (sibling(CHILD,X);sibling(X,CHILD);sister(CHILD,X);sister(X,CHILD);brother(CHILD,X);brother(X,CHILD)).

is_mother_title_assignable(PARENT,CHILD) :- 
     is_parent_of(PARENT,CHILD),
     \+ mother(PARENT, CHILD),
     \+ has_male_title(PARENT).

is_father_title_assignable(PARENT,CHILD) :- 
     is_parent_of(PARENT,CHILD),
     \+ father(PARENT, CHILD),
     \+ has_female_title(PARENT).


is_grandparent_of(GRANDPARENT,X) :- 
     (child(PLACEHOLDER,GRANDPARENT);son(PLACEHOLDER,GRANDPARENT);daughter(PLACEHOLDER,GRANDPARENT)), ( parent(PLACEHOLDER,X); father(PLACEHOLDER,X) ; mother(PLACEHOLDER, X);child(X,PLACEHOLDER);son(X,PLACEHOLDER);daughter(X,PLACEHOLDER);aunt(PLACEHOLDER,X);uncle(PLACEHOLDER,X));
     (parent(GRANDPARENT,PLACEHOLDER);mother(GRANDPARENT,PLACEHOLDER);father(GRANDPARENT,PLACEHOLDER) ), ( parent(PLACEHOLDER,X); father(PLACEHOLDER,X) ; mother(PLACEHOLDER, X);child(X,PLACEHOLDER);son(X,PLACEHOLDER);daughter(X,PLACEHOLDER);aunt(PLACEHOLDER,X);uncle(PLACEHOLDER,X) ).

is_grandmother_title_assignable(GRANDPARENT,X) :- 
     is_grandparent_of(GRANDPARENT,X), 
     \+  grandmother(GRANDPARENT, X),
     \+ has_male_title(GRANDPARENT).

is_grandfather_title_assignable(GRANDPARENT,X) :- 
     is_grandparent_of(GRANDPARENT,X), 
     \+  grandfather(GRANDPARENT, X),
     \+ has_female_title(GRANDPARENT).

is_grandfather_of(GRANDPARENT,X) :-
     grandfather(GRANDPARENT,X);
     father(GRANDPARENT,Z), (parent(Z,X);father(Z,X);mother(Z,X) );
     father(GRANDPARENT,Z), ( child(X,Z);daughter(X,Z);son(X,Z) );
     father(GRANDPARENT,Z), ( aunt(Z,X);uncle(Z,X)).

is_grandmother_of(GRANDPARENT,X) :-
     grandfather(GRANDPARENT,X);
     mother(GRANDPARENT,Z), (parent(Z,X);father(Z,X);mother(Z,X) );
     mother(GRANDPARENT,Z), ( child(X,Z);daughter(X,Z);son(X,Z) );
     mother(GRANDPARENT,Z), ( aunt(Z,X);uncle(Z,X) ).

is_child_of(CHILD,PARENT) :- 
     child(CHILD,PARENT);
     daughter(CHILD,PARENT);
     son(CHILD,PARENT);
     (child(X,PARENT);son(X,PARENT);daughter(X,PARENT) ),(sibling(CHILD,X);sibling(X,CHILD);sister(CHILD,X);sister(X,CHILD);brother(CHILD,X);brother(X,CHILD));
     parent(PARENT,CHILD);
     father(PARENT,CHILD);
     mother(PARENT,CHILD);
     ( parent(PARENT,X); mother(PARENT,X); father(PARENT,X) ),(sibling(CHILD,X);sibling(X,CHILD);sister(CHILD,X);sister(X,CHILD);brother(CHILD,X);brother(X,CHILD)).

is_child_title_assignable(CHILD,PARENT):-
     is_child_of(CHILD,PARENT). 
     
is_daughter_of(CHILD,PARENT) :- 
     daughter(CHILD,PARENT);
     sister(CHILD,X), ( child(X,PARENT);son(X,PARENT);daughter(X,PARENT) );
     sister(CHILD,X), ( parent(PARENT,X);mother(PARENT,X);father(PARENT,X) );
     sister(CHILD,_), ( parent(PARENT,CHILD);mother(PARENT,CHILD);father(PARENT,CHILD) ).

is_son_of(CHILD,PARENT) :- 
     son(CHILD,PARENT), 
     brother(CHILD,X), ( child(X,PARENT);son(X,PARENT);daughter(X,PARENT) );
     brother(CHILD,X), ( parent(PARENT,X);mother(PARENT,X);father(PARENT,X) );
     brother(CHILD,_), ( parent(PARENT,CHILD);mother(PARENT,CHILD);father(PARENT,CHILD) ).


is_daughter_title_assignable(CHILD,PARENT) :- 
     is_child_of(CHILD,PARENT),
     \+ daughter(CHILD,PARENT),
     \+ has_male_title(CHILD).

is_son_title_assignable(CHILD,PARENT) :- 
     is_child_of(CHILD,PARENT),
     \+ son(CHILD,PARENT),
     \+ has_female_title(CHILD).


is_aunt_title_assignable(PIBLING, X) :-
     ( sister(PIBLING,Y); is_sibling_of(PIBLING, Y) ),
     ( is_child_of(X, Y) ; is_parent_of(Y, X) ),
     \+ ( aunt(PIBLING,Y) ; uncle(PIBLING,Y ) ),
     \+ has_male_title(PIBLING). 

is_uncle_title_assignable(PIBLING, X) :-
     ( brother(PIBLING,Y); is_sibling_of(PIBLING, Y) ),
     ( is_child_of(X, Y) ; is_parent_of(Y, X) ),
     \+ ( aunt(PIBLING,X) ; uncle(PIBLING,X ) ),
     \+ has_female_title(PIBLING). 

is_aunt_of(PIBLING,X) :-
     aunt(PIBLING,X);
     sister(PIBLING, Y), is_child_of(X,Y).

is_uncle_of(PIBLING,X) :-
     uncle(PIBLING,X);
     is_sister_of(PIBLING,Y),
     ( is_child_of(X, Y) ; is_parent_of(Y, X) ).

has_male_title(X) :- 
     brother(X,_);
     father(X,_);
     son(X,_);
     grandfather(X,_);
     uncle(X,_).

has_female_title(X) :- 
     sister(X,_);
     mother(X,_);
     daughter(X,_);
     grandmother(X,_);
     aunt(X,_).
     
sister(mary,john).
