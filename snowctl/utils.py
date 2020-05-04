import os


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


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


def parser(cmd: str):
    cmd = cmd.replace('\n', '')
    ls = cmd.split(' ')
    if ls[0] == 'use' and len(ls) != 3:
        return None
    elif ls[0] == 'copy' and ls[1] != 'views':
        return None
    elif ls[0] == 'show' and ls[1] != 'views':
        return None
    elif ls[0] == 'sql' and len(ls) < 2:
        return None
    return ls
