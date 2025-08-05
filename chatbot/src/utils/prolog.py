import sys
sys.path.append("..")

from pyswip import Prolog 
from constants.relationships import prolog_equation

FILE_PATH = '../constants'

def initialize_knowledge_base() -> None:
    """
        Initialize the knowledgebase with the set of rules that were predefined.
    """
    with open(f'{FILE_PATH}/knowledge_base.pl', 'w') as file:
        file.write(prolog_equation)
        file.close()
        


def create_fact(names:tuple[str], relationship:str)->list[str]:
    """
    Creates a valid prolog query from the given names, and relationship. 

    Args:
        names (tuple): Names of the people in the query.
        relationship (str): The relationship to be assigned to the people in the query

    Returns:
        list[str]: A list of valid prolog queries. 
    """
    
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
        
def add_fact(facts:list[str])->None:
    """
    Append the fact to the knowledge base.

    Args:
        facts (list[str]): A list of facts to append to the knowledge base
    """

    
    with open(f'{FILE_PATH}/knowledge_base.pl','a') as file:
        
        for fact in facts:
            fact_not_exist = not fact_exist(fact)
             
            if fact_not_exist:
                file.write(fact.lower() + '\n')
        file.close()

def fact_exist(fact:str)->bool:
    
    """
    Examines wheter fact exist in the knowledgebase. 

    Args:
        fact: the fact to query to the knowledge base 
        
    Returns:
        bool: True if the fact exist in the knowledge base otherwise, it should return False.
    """
    try:
        result = Prolog.query(fact.lower())
        result = list(result)
                
        if result:
            return True
        
        return False
    except:
        return False 

def query_knowledge_base(fact:str)->list[dict]: 
    """
    Query the knowledge base using the fact provided

    Args:
        fact (str): A valid prolog query.

    Returns:
        list[dict]: Result of the query.
    """
     
    try: 
        result = Prolog.query(fact)
        result = list(result)
                
        return result 
    
    except Exception as e:
        return []
