from pyswip import Prolog
from utils.prolog import initialize_knowledge_base
from utils.chatbot import examine_prompt

def main():
    people_pool = set()
    initialize_knowledge_base()    
    print('Welcome to FamBot.')
    
    while (True):
        
        Prolog.consult('../constants/knowledge_base.pl')

        user_prompt = input('Enter a prompt: ')
        examine_prompt(prompt= user_prompt, family_pool=people_pool)


if __name__ == '__main__':
    main()