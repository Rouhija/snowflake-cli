import sys
import signal
import logging
import argparse
from time import sleep
from snowctl.config import Config
from snowctl.connect import snowflake_connect

LOG = logging.getLogger(__name__)

class Controller:
    def __init__(self, conn):
        self.conn = conn
        self.cursor = conn.cursor()
        self.run = True
        self.prompt = 'snowctl> '

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
                self.op_help()
            elif cmd[0] == 'copy' and cmd[1] == 'one':
                self.op_copy_one(cmd)
            elif cmd[0] == 'use':
                self.op_use(cmd)
            return True
        except Exception as e:
            print(e)
            return False

    def op_use(self, cmd: list):
        self.cursor.execute(f"use {cmd[1]} {cmd[2]}")
        response = self.cursor.fetchone()
        print(response[0])        

    def op_copy_one(self, cmd: list):
        resp = self.execute_query('show views')
        for i, row in enumerate(resp):
            print(f'{i} - {row[1]}')
        print('choose the number of the view to copy: ', end='', flush=True)
        view_index = int(sys.stdin.readline().replace('\n', ''))
        target = resp[view_index][1]
        resp = self.execute_query(f"select GET_DDL('view', '{target}')")
        print(resp)

    def op_help(self):
        print('snowctl usage:')
        print('\tuse <database|schema|warehouse> <name>')
        print('\tcopy one')
        print('\tcopy many')

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
            self.op_help()
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
    c = Controller(conn)
    c.run_console()


if __name__ == '__main__':
    main()