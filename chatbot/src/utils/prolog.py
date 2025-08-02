from pyswip import Prolog 

FILE_PATH = '../constants'

def initialize_knowledge_base() -> None:
    with open(f'{FILE_PATH}/knowledge_base.pl', 'w') as file:
        file.write("""
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


is_sibling(X,Y) :- sibling(X,Y);sibling(Y,X);parent(_,Y), parent(_,X); child(X,_),child(Y,_);brother(X,Y);brother(Y,X);sister(X,Y);sister(Y,X).
is_sibling_title_assignable(SIBLING_TO_ASSIGN,X) :- is_sibling(X,X), \+ ( sister(SIBLING_TO_ASSIGN, X) ; brother(SIBLING_TO_ASSIGN, X) ).

is_parent_of(PARENT,CHILD) :- child(CHILD,PARENT); parent(PARENT,CHILD);father(PARENT,CHILD);mother(PARENT,CHILD).
is_parent_title_assignable(PARENT,CHILD) :- is_parent_of(PARENT,CHILD),\+ ( mother(PARENT, CHILD) ; father(PARENT, CHILD) ).

is_grandparent_of(GRANDPARENT,X) :- child(_,GRANDPARENT), parent(_,X);child(_,GRANDPARENT), parent(X,_);parent(GRANDPARENT,_), parent(_,X);parent(GRANDPARENT,_), parent(X,_).
is_grandparent_title_assignable(GRANDPARENT,X) :- is_grandparent_of(GRANDPARENT,X), \+ ( grandmother(GRANDPARENT, X) ; father(GRANDPARENT, X) ).

is_child_of(CHILD,PARENT) :- child(CHILD,PARENT);
     daughter(CHILD,PARENT);son(CHILD,PARENT);
     child(_,PARENT),(
          sibling(CHILD,_);sibling(_,CHILD);sister(CHILD,_);sister(_,CHILD);brother(CHILD,_);brother(_,CHILD));
     parent(PARENT,_),(
          sibling(CHILD,_);sibling(_,CHILD);sister(CHILD,_);sister(_,CHILD);brother(CHILD,_);brother(_,CHILD)).

is_child_title_assignable(CHILD,PARENT) :- is_child_of(CHILD,PARENT), \+ (daughter(CHILD,PARENT);son(CHILD,PARENT)).

is_aunt_title_assignable(PIBLING, X) :-
    is_sibling(PIBLING, _),
    ( is_child_of(X, _) ; is_parent_of(_, X) ),
    ( sister(PIBLING, _) ; \+ uncle(PIBLING,X) ).

is_uncle_title_assignable(PIBLING, X) :-
    is_sibling(PIBLING, _),
    ( is_child_of(X, _) ; is_parent_of(_, X) ),
    ( brother(PIBLING, _) ; \+ aunt(PIBLING,X) ).

""")
        file.close()
        


def create_fact(names:tuple[str], relationship:str)->list[str]:
    
    fact_list = []
    if len(names) == 2:
        fact = f'{relationship}({names[0]},{names[1]}).'
        fact_list.append(fact)
        
    else:
        
        family_members = list(names) 
        owner = family_members.pop()        
        for member in family_members:
            fact_list.append(f'{relationship}({member},{owner}).')
        
    return fact_list
        
def add_fact(facts:list[str]):
    
    with open(f'{FILE_PATH}/knowledge_base.pl','a') as file:
        
        for fact in facts:
            fact_not_exist = not fact_exist(fact)
             
            if fact_not_exist:
                file.write(fact.lower() + '\n')
                file.close()

def fact_exist(fact:str):
    
    try:
        result = Prolog.query(fact.lower())
        result = list(result)
        
        if result:
            return True
        
        return False
    except:
        return False 