import sys
import os.path
from configparser import ConfigParser
from os.path import dirname, realpath

class Config:

    def __init__(self):
        self.work_dir = dirname(realpath(__file__))
        self.config_path = f'{self.work_dir}/config.ini'
        self.config_parser = ConfigParser()

    def write_config(self, rewrite: bool):

        if os.path.isfile(self.config_path):
            config_exists = True
        else:
            config_exists = False

        if rewrite is True or config_exists is False:
            try:
                self.config_parser.read('config.ini')
                self.config_parser.add_section('snowflake')

                account = 'snowflake_account'
                user = 'snowflake_user'
                password = 'snowflake_password'
                wh = 'snowflake_warehouse'

                if config_exists is False:
                    print('First time configuration, please provide following values')

                print('snowflake_account (e.g. "xy12345.east-us-2.azure"): ' , end='', flush=True)
                val = sys.stdin.readline().replace('\n', '')
                self.config_parser.set('snowflake', account, val)
                print('snowflake_user: ' , end='', flush=True)
                val = sys.stdin.readline().replace('\n', '')
                self.config_parser.set('snowflake', user, val)
                print('snowflake_warehouse: ' , end='', flush=True)
                val = sys.stdin.readline().replace('\n', '')
                self.config_parser.set('snowflake', wh, val)
                print('snowflake_password: ' , end='', flush=True)
                val = sys.stdin.readline().replace('\n', '')
                self.config_parser.set('snowflake', password, val)

                with open(self.config_path, 'w') as f:
                    self.config_parser.write(f)
            except KeyboardInterrupt:
                print('\nconfig file was not updated')
            except Exception as e:
                sys.exit(f'error while writing configuration: {e}')
        return

    def read_config(self):
        try:
            r = {}
            self.config_parser.read(self.config_path)
            r['account'] = self.config_parser['snowflake']['snowflake_account']
            r['user'] = self.config_parser['snowflake']['snowflake_user']
            r['wh'] = self.config_parser['snowflake']['snowflake_warehouse']
            r['password'] = self.config_parser['snowflake']['snowflake_password']
            return r
        except KeyError as e:
            sys.exit('missing values in configuration: {e}')