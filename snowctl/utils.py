import re
import os
import sys
from pynput.keyboard import Controller


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


def filter_ddl(ddl, db, schema):
    keyboard = Controller()
    regexp = re.compile('(.*select)(.*)(from.*)', re.IGNORECASE)
    start = regexp.search(ddl).group(1)
    cols = regexp.search(ddl).group(2).strip()
    end = regexp.search(ddl).group(3)
    print(f'\ncurrent columns (target -> {db}.{schema}):\n{cols}\n')
    print('modify columns: ', end='', flush=True)
    keyboard.type(cols)
    user_input = sys.stdin.readline().replace('\n', '').strip()
    new_ddl = f'{start} {user_input} {end}'
    return new_ddl


def parser(cmd: str):
    cmd = cmd.replace('\n', '')
    ls = cmd.split(' ')
    if ls[0] == 'use' and len(ls) != 3:
        return None
    elif ls[0] == 'copy' and ls[1] != 'views':
        return None
    elif ls[0] == 'copy' and len(ls) == 3:
        if ls[2] != 'filter':
            return None
    elif ls[0] == 'show' and ls[1] != 'views':
        return None
    elif ls[0] == 'sql' and len(ls) < 2:
        return None
    return ls
