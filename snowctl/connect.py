import sys
import snowflake.connector

def snowflake_connect(conf):
    print('Connecting to snowflake... ', end='', flush=True)
    try:
        conn = snowflake.connector.connect(
            user=conf['user'],
            password=conf['password'],
            account=conf['account'],
            warehouse=['warehouse']
        )
        print('connected')
        return conn
    except Exception as e:
        sys.exit(e)