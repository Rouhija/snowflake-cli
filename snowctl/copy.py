import sys
from snowctl.utils import *
from snowctl.snowctl import Controller

class Copycat(Controller):
    """
    Subclass of Controller to handle view copying
    """
    def __init__(self, conn, engine, safe):
        super().__init__(conn, engine, safe)

    def prompt_input(self, msg):
        print(msg, end='', flush=True)
        return sys.stdin.readline().replace('\n', '').strip().split(',')

    def get_views(self):
        views = []
        rows = self.execute_query('show views')
        for i, row in enumerate(rows):
            views.append(row[1])
            print(f'{i} - {row[1]}')
        return views

    def select_views(self):
        views = self.get_views()
        user_input = self.prompt_input('choose view(s) to copy ([int, int, ...]|all): ')
        copy_these = []
        if user_input == ['']:
            return None
        elif user_input[0] == 'all':
            copy_these = views
        else:
            for index in user_input:
                copy_these.append(views[int(index)])
        print(f'chose view(s) {", ".join(copy_these)}')
        return copy_these

    def get_ddls(self, views):
        ret = []
        for v in views:
            ddl = self.execute_query(f"select GET_DDL('view', '{v}')")[0][0]
            r = make_overwrite(ddl)
            ret.append(r)
        return ret

    def derive_ddls(self, views, db, schema):
        ret = []
        for v in views:
            columns = self.execute_query(f"show columns in view {db}.{schema}.{v}")
            cols = [c[2] for c in columns]
            r = derive_ddl(cols, db, schema, v)
            ret.append(r)
        return ret

    def get_schemas(self):
        schemas = []
        rows = self.execute_query('show schemas')
        rows.pop(0)  # Ignore information schema
        for i, row in enumerate(rows):
            schemas.append(row[1])
            print(f'{i} - {row[1]}')
        return schemas

    def select_schemas(self):
        schemas = self.get_schemas()
        user_input = self.prompt_input('copy into ([int, int, ...]|all): ')
        copy_into = []
        if user_input == ['']:
            return None
        elif user_input[0] == 'all':
            copy_into = schemas
        else:
            for index in user_input:
                copy_into.append(schemas[int(index)])
        print(f'chose schema(s) {", ".join(copy_into)}')
        return copy_into

    def copy(self, db, schema, derive=False, filter_cols=False, rename=False):
        errors = 0
        clear_screen()

        # sources and destinations
        copy_these = self.select_views()
        if copy_these is None: return None
        copy_into = self.select_schemas()
        if copy_into is None: return None

        # get ddls or get columns if derive
        ddls = self.derive_ddls(copy_these, db, schema) if derive else self.get_ddls(copy_these)

        # copy views from sources to destinations and check flags --rename and --filter
        for i, view in enumerate(copy_these):
            for schema in copy_into:

                # Format query based on flags
                query = format_ddl(ddls[i], view, schema, db)
                if filter_cols is True:
                    query = filter_ddl(query, view, db, schema)
                if rename is True:
                    query = rename_target(query, view, db, schema)

                # Prompt confirmation if -s flag is used
                if self.safe_mode:
                    if not ask_confirmation(query):
                        continue
                
                # Actual query execution
                try:
                    results = self.connection.execute(query)
                    response = results.fetchone()
                except Exception as e:
                    print(e)
                    errors += 1
                    continue
                print(f'{response[0]} (target: {db}.{schema})')
        print(f'\ncopy views finished: {errors} errors\n')
