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
        self.run = True
        self.prompt = 'snowctl> '

    def run_console(self):
        self.listen_signals()
        try:
            while self.run:
                print(self.prompt, end='', flush=True)
                cmd = sys.stdin.readline().replace('\n', '')
                cmd = self.parse(cmd)
                if cmd is None:
                    self.run = False
                self.operation(cmd)
        finally:
            self.exit_console()

    def operation(self, cmd: list):
        try:
            if cmd[0] == 'help':
                self.op_help()
            elif cmd[0] == 'copy':
                self.op_copy(cmd)
            return True
        except Exception as e:
            return False

    def op_copy(self, cmd: list):
        print('copy')

    def op_help(self):
        print('commands')

    def parse(self, cmd: str):
        ls = cmd.split(' ')
        return ls

    def exit_console(self):
        try:
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