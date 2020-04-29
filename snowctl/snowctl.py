import sys
import signal
import logging
import argparse
from time import sleep
from snowctl.config import Config
from snowctl.utils import clear_screen, format_ddl
from snowctl.connect import snowflake_connect

LOG = logging.getLogger(__name__)

class Controller:
    def __init__(self, conn, safe):
        self.conn = conn
        self.cursor = conn.cursor()
        self.safe_mode = safe
        self.run = True
        self.prompt = 'snowctl> '
        self.curr_db = None

    def run_console(self):
        self.listen_signals()
        try:
            while self.run:
                self.get_prompt()
                print(self.prompt, end='', flush=True)
                cmd = sys.stdin.readline()
                cmd = self.parse(cmd)
                if cmd is not None:
                    self.operation(cmd)
        except Exception as e:
            LOG.error(e)
        finally:
            self.exit_console()

    def operation(self, cmd: list):
        try:
            if cmd[0] == 'help':
                self.usage()
            elif cmd[0] == 'copy':
                self.copy_views()
            elif cmd[0] == 'show':
                self.show_views()
            elif cmd[0] == 'use':
                self.use(cmd)
            elif cmd[0] == 'exit':
                self.exit_console()
            return True
        except Exception as e:
            print('Error, try again.')
            print(e)
            return False

    def use(self, cmd: list):
        self.cursor.execute(f"use {cmd[1]} {cmd[2]}")
        response = self.cursor.fetchone()
        print(response[0])        

    def show_views(self):
        rows = self.execute_query('show views')
        for i, row in enumerate(rows):
            print(f'{i} - {row[1]}')

    def copy_views(self):
        clear_screen()

        # Prompt for view(s) to copy
        views = []
        rows = self.execute_query('show views')
        for i, row in enumerate(rows):
            views.append(row[1])
            print(f'{i} - {row[1]}')
        print('choose view(s) to copy ([int, int, ...]|all): ', end='', flush=True)
        user_input = sys.stdin.readline().replace('\n', '').strip().split(',')

        # Choose views
        copy_these = []
        if user_input[0] == 'all':
            copy_these = views
        else:
            for index in user_input:
                copy_these.append(views[int(index)])

        # Get ddl for chosen views
        print(f'chose view(s) {", ".join(copy_these)}')
        ddls = []
        for copy_this in copy_these:
            ddls.append(self.execute_query(f"select GET_DDL('view', '{copy_this}')")[0][0].replace('\n', ''))
        
        # Prompt for schema(s) to copy into
        schemas = []
        rows = self.execute_query('show schemas')
        for i, row in enumerate(rows):
            if row[1] == 'INFORMATION_SCHEMA':
                continue
            schemas.append(row[1])
            print(f'{i} - {row[1]}')
        print(f'copy into to ([int, int, ...]|all): ', end='', flush=True)
        user_input = sys.stdin.readline().replace('\n', '').strip().split(',')

        # Choose schemas
        copy_into = []
        if user_input[0] == 'all':
            copy_into = schemas
        else:
            for index in user_input:
                copy_into.append(schemas[int(index)])

        # Execute
        print(f'chose schema(s) {", ".join(copy_into)}')
        for i, view in enumerate(copy_these):
            for schema in copy_into:
                query = format_ddl(ddls[i], view, schema, self.curr_db)
                if self.safe_mode:
                    y = self.ask_confirmation(query)
                    if not y:
                        continue
                self.cursor.execute(query)
                response = self.cursor.fetchone()
                print(f'{response[0]} ({self.curr_db}.{schema})')

    def ask_confirmation(self, query):
        print(f'\n{query}')
        print(f'Confirm? (y/n): ', end='', flush=True)
        user_input = sys.stdin.readline().replace('\n', '').strip()
        if user_input == 'y':
            return True
        else:
            return False

    def usage(self):
        print('snowctl usage:')
        print('\tuse <database|schema|warehouse> <name>')
        print('\tcopy views (in current context)')
        print('\tshow views (in current context)')
        print('\texit')

    def execute_query(self, query):
        LOG.debug(f'executing:\n{query}')
        self.cursor.execute(query)
        results = []
        while True:
            row = self.cursor.fetchone()
            if not row:
                break
            results.append(row)
        return results

    def parse(self, cmd: str):
        cmd = cmd.replace('\n', '')
        ls = cmd.split(' ')
        if ls[0] == 'use' and len(ls) != 3:
            self.usage()
            return None
        elif ls[0] == 'copy' and ls[1] != 'views':
            self.usage()
            return None
        elif ls[0] == 'show' and ls[1] != 'views':
            self.usage()
            return None
        return ls

    def get_prompt(self):
        prompt = ''
        response = self.execute_query('select current_warehouse(), current_database(), current_schema()')
        wh = response[0][0]
        db = response[0][1]
        schema = response[0][2]
        if wh is not None:
            prompt += f'{wh}:'
        if db is not None:
            prompt += f'{db}:'
            self.curr_db = db
        if schema is not None:
            prompt += f'{schema}:'
        if not len(prompt):
            self.prompt = 'snowctl> '
        else:
            prompt = prompt[:-1]
            self.prompt = f'{prompt}> '.lower()

    def exit_console(self):
        print('closing connections...')
        try:
            self.cursor.close()
            self.conn.close()
        finally:
            sys.exit('exit')

    def listen_signals(self):
        signal.signal(signal.SIGINT, self.signal_handler)
        signal.signal(signal.SIGTERM, self.signal_handler)

    def signal_handler(self, signum, frame):
        if signum == signal.SIGINT or signum == signal.SIGTERM:
            self.exit_console()           


def arg_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--debug", help="log to console", action="store_true")
    parser.add_argument("-s", "--safe", help="ask for confirmation before executing any operations", action="store_true")
    parser.add_argument("-c", "--configuration", help="re-input configuration values", action="store_true")
    return parser.parse_args()


def logger_options(debug: int):
    if debug:
        logging.basicConfig(
            level=logging.DEBUG,
            format='%(levelname)s:%(asctime)s ⁠— %(message)s',
            datefmt='%d/%m/%Y %H:%M:%S'
    )
    else:
         logging.basicConfig(
            level=logging.ERROR,
            format='%(levelname)s:%(asctime)s ⁠— %(message)s',
            datefmt='%d/%m/%Y %H:%M:%S'
    )       


def main():
    args = arg_parser()
    conf = Config()
    conf.write_config(args.configuration)
    logger_options(args.debug)
    conn = snowflake_connect(conf.read_config())
    c = Controller(conn, args.safe)
    c.run_console()


if __name__ == '__main__':
    main()