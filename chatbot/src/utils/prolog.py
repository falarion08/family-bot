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


sibling(rizz,sigma).
male(rizz).
parent(sigma,ligma).



are_siblings(X,Y) :- sibling(X,Y);sibling(Y,X);parent(_,Y), parent(_,X); child(X,_),child(Y,_).

is_parent(PARENT,CHILD) :- child(CHILD,PARENT); parent(PARENT,CHILD).
is_grandparent_of(GRANDPARENT,X) :- child(_,GRANDPARENT), parent(_,X);child(_,GRANDPARENT), parent(X,_);parent(GRANDPARENT,_), parent(_,X);parent(GRANDPARENT,_), parent(X,_).
is_gender_defined(X) :- male(X);female(X).
is_parent_title_assignable(PARENT,CHILD) :- is_parent(PARENT,CHILD), is_gender_defined(PARENT).

sister(SIBLING,X) :- are_siblings(X,SIBLING), female(SIBLING). 
brother(SIBLING,X) :- are_siblings(X,SIBLING), male(SIBLING). 

mother(PARENT,CHILD) :- is_parent(PARENT,CHILD), female(PARENT).
father(PARENT,CHILD) :- is_parent(PARENT,CHILD), male(PARENT).

grandmother(GRANDPARENT,X) :- is_grandparent_of(GRANDPARENT,X), female(X).
grandfather(GRANDPARENT,X) :- is_grandparent_of(GRANDPARENT,X), male(X).

aunt(PIBLING,X) :- sister(_,PIBLING), child(X,_); sister(_,PIBLING), parent(_,X).
uncle(PIBLING,X) :- brother(PIBLING,_), child(X,_); brother(PIBLING,_), parent(_,X).
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
    
    with open(f'{FILE_PATH}/knowledge_base.pl','w') as file:
        
        for fact in facts:
            fact_not_exist = not fact_exist(fact)
             
            if fact_not_exist:
                file.write(fact)
                file.close()

def fact_exist(fact:str):
    
    try:
        result = Prolog.query(fact)
        result = list(result)
        
        if result:
            return True
        
        return False
    except:
        return False 