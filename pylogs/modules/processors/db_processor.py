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
            con_obj.commit()
            return True
        except Exception as create_users_table_error:
            self.exception_process.log_error(create_users_table_error)
            return False


    def create_events_table(self, con_obj) -> bool:
        try:
            con_obj.cursor().execute(
                self.prt.sql_statement(self.create_events_table.__name__)
            )
            con_obj.commit()
            return True
        except Exception as create_events_table_error:
            self.exception_process.log_error(create_events_table_error)
            return False


    def get_tables(self, con_obj) -> list:
        """
        Returns: ['table1', 'table2', ... ]
        """
        try:
            return [table[0] for table in con_obj.cursor().execute(
                self.prt.sql_statement(self.get_tables.__name__))]
        except Exception as fetch_tables_error:
            self.exception_process.log_error(fetch_tables_error)


    def create_user(self, con_obj, user_obj) -> bool:
        try:
            con_obj.cursor().execute(
                self.prt.sql_statement(self.create_user.__name__),
                (
                    user_obj.secret_key,
                    user_obj.secret_iv,
                    user_obj.username,
                    user_obj.pass_hash
                )
            )
            con_obj.commit()
            return True
        except Exception as create_user_error:
            self.exception_process.log_error(create_user_error)
            return False


    def check_if_user_exists(self, con_obj, username) -> bool:
        try:
            res = con_obj.cursor().execute(
                self.prt.sql_statement(
                    self.check_if_user_exists.__name__),
                    (username,)
                )
            data = res.fetchone()
            return False if data is None else True
            
            
        except Exception as user_check_error:
            self.exception_process.log_error(user_check_error)


    def get_user_object(self, con_obj, username=None) -> tuple:
        """
        Returns:
            (<secret_key>, <secret_iv>, <username>, <pass_hash>)
        """
        try:
            user_object = con_obj.cursor().execute(
                self.prt.sql_statement(
                    self.get_user_object.__name__),
                    (username,)).fetchone()
            return user_object
            
        except Exception as get_user_obj_error:
            self.exception_process.log_error(get_user_obj_error)
            

    def add_event(self, con_obj, event_log: list) -> bool:
        try:
            con_obj.cursor().execute(
                self.prt.sql_statement(self.add_event.__name__),
                (
                    str(event_log[0]),
                    str(event_log[1]),
                    str(event_log[2]),
                    str(event_log[3]),
                    str(event_log[4]),
                    str(event_log[5]),
                    str(event_log[6]),
                    str(event_log[7])
                )
            )
            con_obj.commit()
            return True
        except Exception as add_event_error:
            self.exception_process.log_error(add_event_error)
            return False


    def fetch_event(self, con_obj, creator) -> list:
        """
        event_log -> [
            (
                '00/00/00',
                '00:00:00', 
                'title', 
                'tst', 
                'event_user', 
                'event_staff', 
                'event_data', 
                'creator'
            ),
            ...
        ]
        """
        try:
            event_log = con_obj.cursor().execute(
                self.prt.sql_statement(self.fetch_event.__name__),
                (creator,)).fetchall()
            return event_log
        except Exception as fetch_event_error:
            self.exception_process.log_error(fetch_event_error)


    def search_events(self, event_log, keyword) -> tuple:
        """ Expects unencrypted event_log """
        events_found = ()
        for event_tuple in event_log:
            for data_type in event_tuple:
                    if keyword in data_type:
                        events_found += event_tuple
        return events_found




        
