

import re 
FILE_PATH = '../constants'

def create_fact(names:tuple[str], relationship:str):
    
    print(names)
    if len(names) == 2:
        fact = f'{relationship}({names[0]},{names[1]}).'

        add_fact(fact)
    else:
        # query = r'child|parent'
        # query_result = re.search(query,relationship)
        
        # base_relationship_name = query_result.group()
        family_members = list(names) 
        owner = family_members.pop()
        
        fact = ''
        
        for member in names:
            fact = fact + f'{relationship}({member},{owner}).' + '\n'
        
        add_fact(fact)    
        
def add_fact(fact:str):
    with open(f'{FILE_PATH}/knowledge_base.pl','a') as file:
        file.write(fact)
        file.close()
    
valid_sentence_prompts = [
    r'(\w+) and (\w+) are siblings',
    r'(\w+) is a (?:sister|child|brother|grandfather|grandmother|son|daughter|aunt) of (\w+)',
    r'(\w+) is the (?:mother|father) of (\w+)',
    r'(\w+) is an (?:uncle|aunt) of (\w+)',
    r'(\w+), (\w+) and (\w+) are children of (\w+)',
    r'(\w+) and (\w+) are the parents of (\w+)'
]

family_titles = ['sibling','sister','mother','grandmother','child','uncle','brother','father','parent','grandfather','children','son','aunt']



def examine_prompt(prompt:str, family_pool:set):
    for filter in valid_sentence_prompts: 
        query_result = re.match(filter,prompt,re.IGNORECASE)
        
        if query_result:
            result = query_result
            
            title = extract_family_title(prompt)
            names = result.groups()
            
            create_fact(names,title)
            
            return query_result
        
def extract_family_title(prompt:str) -> str:
    re_filter = r'' + family_titles[0]
    
    for title in family_titles[1:]:
        re_filter = re_filter + '|' + title
    
    result = re.search(re_filter,prompt,re.IGNORECASE)
    family_title = result.group()
    
    return family_title      


result = examine_prompt('kylan and dan are the parents of X')


