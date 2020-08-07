import sys
import getpass
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
                wh = 'default_warehouse'
                db = 'default_database'
                curr_acc = None
                curr_user = None
                curr_wh = None
                curr_db = None
                curr_pw = None

                if config_exists is False:
                    print('First time configuration, please provide following values')
                else:
                    try:
                        self.config_parser.read(self.config_path)
                        curr_acc = self.config_parser['snowflake']['snowflake_account']
                        curr_user = self.config_parser['snowflake']['snowflake_user']
                        curr_wh = self.config_parser['snowflake']['default_warehouse']
                        curr_db = self.config_parser['snowflake']['default_database']
                        curr_pw = self.config_parser['snowflake']['snowflake_password']
                        if curr_pw: curr_pw = '*****'
                    except:
                        pass

                print(f'snowflake_account ({curr_acc}): ' , end='', flush=True)
                val = sys.stdin.readline().replace('\n', '').replace('.snowflakecomputing.com', '')
                if val != '':
                    self.config_parser.set('snowflake', account, val)
                print(f'snowflake_user ({curr_user}): ' , end='', flush=True)
                val = sys.stdin.readline().replace('\n', '')
                if val != '':
                    self.config_parser.set('snowflake', user, val)
                print(f'default_warehouse ({curr_wh}): ' , end='', flush=True)
                val = sys.stdin.readline().replace('\n', '')
                if val != '':
                    self.config_parser.set('snowflake', wh, val)
                print(f'default_database ({curr_db}): ' , end='', flush=True)
                val = sys.stdin.readline().replace('\n', '')
                if val != '':
                    self.config_parser.set('snowflake', db, val)
                val = getpass.getpass(f'snowflake_password ({curr_pw}): ')
                if val != '':
                    self.config_parser.set('snowflake', password, val)

                with open(self.config_path, 'w') as f:
                    self.config_parser.write(f)
                print('Configuration written')
            except KeyboardInterrupt:
                sys.exit('\nconfig file was not updated')
            except Exception as e:
                sys.exit(f'error while writing configuration: {e}')
        return

    def read_config(self):
        try:
            r = {}
            self.config_parser.read(self.config_path)
            r['account'] = self.config_parser['snowflake']['snowflake_account']
            r['user'] = self.config_parser['snowflake']['snowflake_user']
            r['warehouse'] = self.config_parser['snowflake']['default_warehouse']
            r['database'] = self.config_parser['snowflake']['default_database']
            r['password'] = self.config_parser['snowflake']['snowflake_password']
            return r
        except KeyError as e:
            sys.exit(f'missing values in configuration: {e}')

    def echo_config(self):
        c = self.read_config()
        print('\ncurrent configuration')
        for k, v in c.items():
            if k == 'password':
                v = '*****'
            print(f'  {k}: {v}')
