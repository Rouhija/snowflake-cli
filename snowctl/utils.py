import os

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def format_ddl(ddl, view_name, target_schema, database):
    tokens = ddl.split(' ')
    for i, token in enumerate(tokens):
        if token == 'view':
            tokens[i + 1] = f'{database}.{target_schema}.{view_name}'
            break
    new_ddl = ' '.join(tokens)
    return new_ddl