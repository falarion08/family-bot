import sys
sys.path.append('..')
from pyswip import Prolog
from utils.regex import get_prompt_type,extract_relationship,extract_names_from_prompt
from utils.prolog import create_fact,fact_exist,add_fact


def examine_prompt(prompt:str, family_pool:set): 
    
    prompt_result  = get_prompt_type(prompt)
    
    if prompt_result:

        prompt_type, regex_match = prompt_result['query_type'], prompt_result['regex_match']
        
        if prompt_type == 'statement':

            if regex_match:
                
                relationship = extract_relationship(prompt)
                names = extract_names_from_prompt(regex_match)
                
                if fact_duplicated(names,relationship):
                    print('I already knew that!')
                elif validate_kb_insertion(names,relationship,family_pool):
                    
                    facts = create_fact(names,relationship)
                    add_fact(facts)
                    update_family_pool(names,family_pool)
                    
                    print('OK! I learned something new.')
                else:
                    print("That's impossible")
                
    else:
        print('Invalid prompt. Kindly check spelling, and proper casing of the letters.')

def update_family_pool(names:tuple, family_pool:set):
    for name in names:
        family_pool.add(name)
        
def validate_kb_insertion(names:tuple, relationship: str, family_pool:set)->bool: 
    
    count = count_pool_members(names,family_pool)
    distinct_names_count = len(set(names))
    

    notable_titles = {'sister','brother','grandmother','grandfather','mother','father'}
    family_title_to_gender_neutral = {'mother':'parent','father':'parent','sister':'sibling','brother':'sibling',
                                      'grandfather':'grandparent','grandmother':'grandparent'}
    

    
    if distinct_names_count == len(names):
        prefix = ''
        suffix = ''
        
        if count == 2:
            prefix = 'is_'
            suffix = f'_title_assignable({names[0],names[1]}).'
            
            if relationship in notable_titles:
                relationship = family_title_to_gender_neutral[relationship]
        
        query = prefix + relationship + suffix
        
        if count >= 2:

            if count == 2 and fact_exist(query):
                return True
                
        else:
            return True
    
    return False

def fact_duplicated(names:tuple, relationship:str)->bool:
    
    prolog_queries = create_fact(names,relationship)
    
    print(prolog_queries)
    
    for query in prolog_queries: 
        
        query = query.removesuffix('.')
        
        not_existing_fact = not fact_exist(query)
        
        if not_existing_fact:
            return False
        
    return True
    

def count_pool_members(names:tuple, family_pool:set)->int: 
    count = 0
    for name in names:
        if name in family_pool:
            count = count + 1
    return count
    
                
            
            
    
    
    