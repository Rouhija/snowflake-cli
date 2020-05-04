import sys
import signal
import logging
from time import sleep
from snowctl.config import Config
from snowctl.arguments import arg_parser
from snowctl.logger import logger_options
from snowctl.connect import snowflake_connect
from snowctl.utils import bcolors, clear_screen, format_ddl, parser


LOG = logging.getLogger(__name__)


def print_usage():
    print('\nsnowctl usage:')
    print('\tuse <database|schema|warehouse> <name>')
    print('\tcopy views (in current context)')
    print('\tshow views (in current context)')
    print('\tsql <query>')
    print('\texit|ctrl+C\n')


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
        print_usage()
        try:
            while self.run:
                self.get_prompt()
                print(f'{bcolors.OKBLUE}{self.prompt}{bcolors.ENDC}', end='', flush=True)
                cmd = sys.stdin.readline()
                cmd = parser(cmd)
                if cmd is not None:
                    self.operation(cmd)
                else:
                    print_usage()
        except Exception as e:
            LOG.error(e)
        finally:
            self.exit_console()

    def operation(self, cmd: list):
        try:
            if cmd[0] == 'help':
                print_usage()
            elif cmd[0] == 'copy':
                self.copy_views()
            elif cmd[0] == 'show':
                self.show_views()
            elif cmd[0] == 'use':
                self.use(cmd)
            elif cmd[0] == 'sql':
                self.user_query(cmd)
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

    def user_query(self, cmd: list):
        cmd.pop(0)
        query = ' '.join(cmd)
        response = self.execute_query(query)
        for row in response:
            print(row)

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
                print(f'{response[0]} (target: {self.curr_db}.{schema})')

    def ask_confirmation(self, query):
        print(f'\n{query}')
        print(f'Confirm? (y/n): ', end='', flush=True)
        user_input = sys.stdin.readline().replace('\n', '').strip()
        if user_input == 'y':
            return True
        else:
            return False

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
