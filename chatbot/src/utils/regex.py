
import re
from re import Match
from constants.relationships import valid_sentence_prompts,relationships


def get_prompt_type(prompt:str)->dict|None:
    for filter in valid_sentence_prompts: 
        query_result = re.match(filter,prompt,re.IGNORECASE)

        if query_result:
            result = query_result
            query_type = 'statement'
            
            if filter.endswith('?'):
                query_type = 'question'
            
            return {
                'query_type':query_type,
                'regex_match' : result
                }
        
def extract_relationship(prompt:str) -> str:
    re_filter = r'' + relationships[0]
    
    for title in relationships[1:]:
        re_filter = re_filter + '|' + title
    
    result = re.search(re_filter,prompt,re.IGNORECASE)
    relationship = result.group()
    
    return relationship

def extract_names_from_prompt(result: Match[str]):
    names = result.groups()
    return names   

