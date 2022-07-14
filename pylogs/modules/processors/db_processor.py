import sqlite3


class DbProcessor:
    def __init__(self,
        user=None, 
        setup_cfg=None, 
        exception_process=None,
        prt=None,
    ):
        self.user = user
        self.setup_cfg = setup_cfg
        self.exception_process = exception_process
        self.prt = prt

    
    def connect(self) -> sqlite3.Connection:
        try:
            connection_object = sqlite3.connect(
                f"{self.setup_cfg.db_path}{self.setup_cfg.db_name}"
            )
            return connection_object

        except Exception as db_connect_error:
            self.exception_process.log_error(db_connect_error)


    def create_users_table(self, con_obj) -> bool:
        try:
            con_obj.cursor().execute(
                self.prt.sql_statement(self.create_users_table.__name__)
            )
            return True
        except Exception as create_users_table_error:
            self.exception_process.log_error(create_users_table_error)
            return False


    def create_events_table(self, con_obj) -> bool:
        try:
            con_obj.cursor().execute(
                self.prt.sql_statement(self.create_events_table.__name__)
            )
            return True
        except Exception as create_events_table_error:
            self.exception_process.log_error(create_events_table_error)
            return False


    def get_tables(self, con_obj) -> list:
        """
        Returns --> ['table1', 'table2', ... ]
        """
        tables = [table[0] for table in con_obj.cursor().execute(
            "SELECT name FROM sqlite_master WHERE type='table';"
        )]
        return tables
