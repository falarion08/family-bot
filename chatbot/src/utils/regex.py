
import re
from re import Match
from constants.relationships import valid_sentence_prompts,relationships


def get_prompt_type(prompt:str)->dict|None:
    """
    Get the type of prompt user 

    Args:
        prompt (str): _description_

    Returns:
        dict|None: Returns the type of prompt of the user and the match regex filter
    """
    for filter in valid_sentence_prompts: 
        query_result = re.match(filter,prompt,re.IGNORECASE)


        if query_result:
            result = query_result
            query_type = 'statement'
                        
            if prompt.endswith('?'):
                query_type = 'question'
                
            return {
                'query_type':query_type,
                'regex_match' : result
                }
        
def extract_relationship(prompt:str) -> str:
    """
    Extract the relationship title from the prompt

    Args:
        prompt (str): The prompt of the user which is either a statement or a question

    Returns:
        str: The name of the relationship between two users. 
    """
    re_filter = r'' + relationships[0]
    
    for title in relationships[1:]:
        re_filter = re_filter + '|' + title
    
    result = re.search(re_filter,prompt,re.IGNORECASE)
    relationship = result.group()
    
    return relationship

def extract_names_from_prompt(result: Match[str]) -> tuple[str | None]:
    """
    Extract all names from a prompt of the user

    Args:
        result (Match[str]): A regex match which contains the names of the people in the prompt 

    Returns:
        tuple[str | None]: The names of the individual returned as a tuple. 
    """
    names = result.groups()
    return names   

