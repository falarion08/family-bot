FILE_PATH = '../constants'
def initialize_knowledge_base() -> None:
    with open(f'{FILE_PATH}/knowledge_base.pl', 'w') as file:
        file.write('')
        file.close()