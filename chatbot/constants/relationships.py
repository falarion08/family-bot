# Prolog queries to verify the relationship between two given individuals
validation_family_title_queries = {
    'sibling':['parent(Z,X), parent(Z,Y).','mother(Z,X), mother(Z,Y)','father(Z,X), father(Z,Y).','sibling(Y,X).','brother(X,Y).','brother(Y,X).','sister(X,Y).','sister(Y,X).'],
    'sister':['sibling(X,Y), female(X).','brother(Y,X), female(X).'],
    'brother':['sibling(X,Y), male(X).','sister(Y,X), male(X).'],
    'child':['parent(Y,X).','mother(Y,X).','father(Y,X).'],
    'daughter':['parent(Y,X), female(X).','mother(Y,X), female(X).','father(Y,X), female(X).'],
    'son':['parent(Y,X), male(X).','mother(Y,X), male(X).','father(Y,X), male(X).'],
    'parent':['child(Y,X).', 'daughter(Y,X).','son(X,Y).'],
    'mother':['child(Y,X), female(X).','daughter(Y,X),female(X).','son(Y,X),female(X).'],
    'father':['child(Y,X), male(X).','daughter(Y,X),male(X).','son(Y,X),male(X).'],
    'grandmother':[],
    'grandfather':[],
    'uncle':[],
    'aunt':[]
}

valid_sentence_prompts = [
    r'(\w+) and (\w+) are siblings.',
    r'(\w+) is a (?:sister|child|brother|grandfather|grandmother|son|daughter|aunt) of (\w+).',
    r'(\w+) is the (?:mother|father) of (\w+).',
    r'(\w+) is an (?:uncle|aunt) of (\w+).',
    r'(\w+), (\w+) and (\w+) are children of (\w+).',
    r'(\w+) and (\w+) are the parents of (\w+).'
]

relationships = [
                'sibling','sister','mother',
                 'grandmother','child','uncle','brother',
                 'father','parent','grandfather',
                 'son','aunt'
                 ]

    