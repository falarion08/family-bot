from pyswip import Prolog 

FILE_PATH = '../constants'

def initialize_knowledge_base() -> None:
    with open(f'{FILE_PATH}/knowledge_base.pl', 'w') as file:
        file.write("""
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