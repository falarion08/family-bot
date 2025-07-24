from pyswip import Prolog
from utils.prolog import initialize_knowledge_base

Prolog.consult('knowledge.pl')


def main():
    initialize_knowledge_base()
    
    print('Welcome to FamBot.')
    while (True):
        input('Enter a prompt: ')
        
    
    

if __name__ == '__main__':
    main()
    
    