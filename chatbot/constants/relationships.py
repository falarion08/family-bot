# Prolog queries to verify the relationship between two given individuals
validation_family_title_queries = {
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
                 'father','parent','grandfather','daughter',
                 'son','aunt'
                 ]

    