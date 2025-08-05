import sys
sys.path.append('..')
from utils.regex import get_prompt_type,extract_relationship,extract_names_from_prompt
from utils.prolog import create_fact,fact_exist,add_fact,query_knowledge_base
from constants.relationships import sentence_format,male_roles,female_roles


def examine_prompt(prompt:str, family_pool:set) -> None: 
    """
    This function handles the prompt of the user and produce the proper output depending on the user prompt.

    Args:
        prompt (str): The prompt of the user which is either a statement or a question.
        family_pool (set): A set of people to know who are already exist in the family tree.
    """
    
    prompt_result  = get_prompt_type(prompt)
    
    if prompt_result:

        prompt_type, regex_match = prompt_result['query_type'], prompt_result['regex_match']

        relationship = extract_relationship(prompt)
        names = extract_names_from_prompt(regex_match)

        if prompt_type == 'statement':

            if regex_match:                
                
                # Examines if the fact already exist in the knowledge base.
                if fact_duplicated(names,relationship):
                    print('I already knew that!')
                
                # Handles appending to the knowledge base if the relationship is valid
                elif validate_kb_insertion(names,relationship,family_pool):
                    
                    facts = create_fact(names,relationship)
                    add_fact(facts)
                    update_family_pool(names,family_pool) # Adds the names of individuals to the knowledge pool.
                    
                    print('OK! I learned something new.')
                    
                else:
                    print("That's impossible")
                    
        elif prompt_type == 'question':

            name_to_query = extract_names_from_prompt(regex_match)[0].lower()
            
            
            if regex_match:
                
                if prompt.startswith("Who"):
                    
                    query = f'is_{relationship}_of(X,{name_to_query.lower()}).' 
                    result = query_knowledge_base(query) 
                    
                    data = extract_data_from_prolog_query_result(result)

                    if len(data) == 0: 
                        print('No information existing for this query yet.')
                    else:
                        print(f'The {sentence_format[relationship]} of {name_to_query}: ' + ', '.join(data))
                
                else: 
                    relationship_exist = relationship_checker(names,relationship)
                    
                    if relationship_exist:
                        print('yes')
                    else: 
                        print('no')
    else:
        print('Invalid prompt. Kindly check spelling, and proper casing of the letters.')

def update_family_pool(names:tuple, family_pool:set) -> None:
    """
    Add a string of names into the family pool set

    Args:
        names (tuple): The names of the people to add in the family pool
        family_pool (set): The set of people already exist in the family tree.
    """
    for name in names:
        family_pool.add(name)
        
def validate_kb_insertion(names:tuple, relationship: str, family_pool:set)->bool: 
    """
    This function examines whether the prompt is a valid relationship or an an impossible relationship. 

    Args:
        names (tuple): Names of the people in the query.
        relationship (str): The relationship to be assigned to the people in the query
        family_pool (set): A set of people who already exist in the database

    Returns:
        bool: True if the relationship is valid and add them to the knowledge base, otherwise it should be false. 
    """
    
    count = count_pool_members(names,family_pool)
    distinct_names_count = len(set(names))

    # Handler if there are no duplicates of name in the query.
    if distinct_names_count == len(names): 

        if count >= 1:
            query = f'is_{relationship}_title_assignable({names[0]},{names[1]}).'
            
            if count <= 2:
                
                if count == 1: # This handles when only one person exist in the family pool, and check what gender is assigned to them.
                    if relationship in female_roles:
                        has_male_title = fact_exist(f'has_male_title({names[0]}).')
                        has_female_title = fact_exist(f'has_female_title({names[0]}).')

                        if (not has_male_title and has_female_title) or (not has_male_title and not has_female_title):
                            return True
                    elif relationship in male_roles:
                        has_male_title = fact_exist(f'has_male_title({names[0]}).')
                        has_female_title = fact_exist(f'has_female_title({names[0]}).')

                        if (has_male_title and not has_female_title) or (not has_male_title and not has_female_title):
                            return True
                    else:
                        return True
                else:    
                    if fact_exist(query):
                        return True
            
            else:
                # Handles if there are at least 3 names in the statement query
                names_list:list[str] = list(names)
                name_to_check_relationship_with = names_list.pop()
                
                for name_to_verify in names_list:
                    
                    query = f'is_{relationship}_of({name_to_verify},{name_to_check_relationship_with})'
                    
                    if name_to_verify in family_pool and name_to_check_relationship_with in family_pool:
                        
                        # Checks remaining individuals if a possible relationship is valid with the person they are being assigned a relationship with if both of them exist
                        
                        is_relationship_impossible = not fact_exist(query)
                        
                        if is_relationship_impossible:
                            return False

                # Special test verification to check if all 3 children of the parent are siblings
                if relationship == 'child':
                    
                    for i,person in enumerate(names_list):
                        for person_to_verify in names_list[i:]:
                            
                            if person in family_pool and person_to_verify in family_pool:
                                query = f'is_sibling_of({person.lower()},{person_to_verify.lower()})'
                                
                                if not fact_exist(query):
                                    return False
                return True
        else:
            return True
    
    return False

def fact_duplicated(names:tuple, relationship:str)->bool:
    
    """ 
     This function examines whether the exact relationship between the provided names already exist in the knowledge base.
   
    Args:
        names (tuple): Names of the people in the query.
        relationship (str): The relationship to be assigned to the people in the query

    Returns:
        bool: True if the information exist, otherwise it is False.
    """
    
    prolog_queries = create_fact(names,relationship)
        
    for query in prolog_queries: 
        
        query = query.removesuffix('.')
        
        not_existing_fact = not fact_exist(query)
        
        if not_existing_fact:
            return False
        
    return True

def count_pool_members(names:tuple, family_pool:set)->int: 
    """
    Count the number of names from the prompt that are already in the family pool set. 

    Args:
        names (tuple): Names of the people in the query.
        family_pool (set): A set of people who already exist in the database

    Returns:
        int: Number of people who already exist in the family pool.
    """
    count = 0
    for name in names:
        if name in family_pool:
            count = count + 1
    return count
    
def extract_data_from_prolog_query_result(query_result:list[dict])->list[str]:
    """
    Returns a list of string that contains the name of people that was obtained from the prolog query.

    Args:
        query_result (list[dict]): The data directly obtained from running a query using Pyswip

    Returns:
        list[str]: The list of individuals from the query
    """
    
    results = []
    
    if len(query_result) > 0:
        for item in query_result:
            
            item = list(item.values())
            item = item[0]
            
            results.append(item)
            
    return results

def relationship_checker(names:tuple,relationship:tuple) -> bool:
    """
    Examines the relationship between the names provided. It checks wheter the person is a sister of another person,
    and other relationships. 

    Args:
        names (tuple): Names of the people in the query.
        relationship (str): The relationship to be assigned to the people in the query

    Returns:
        bool: True if a relationship exist between the names provided, otherwise it should be false. 
    """
    name_list = list(names) 
    
    name_to_check_with = name_list.pop()
    
    for name in name_list:
        query = f'is_{relationship}_of({name},{name_to_check_with}).'
        
        if not fact_exist(query):
            return False
    
    return True 
    
        
    
    
    