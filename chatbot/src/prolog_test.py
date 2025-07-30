from pyswip import Prolog

print('hello')
Prolog.consult('kb.pl')

result = Prolog.query(('sibling(sigma,skibidi).'))

result = list(result)

print(result)