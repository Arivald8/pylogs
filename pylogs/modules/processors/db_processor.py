import sqlite3

from ..pylogs_setup import PylogsSetup
from .exception_processor import ExceptionProcessor
from ..printer_model import Printer

exception_process = ExceptionProcessor()
prt = Printer()


class DbProcessor:
    def __init__(self, user=None, setup_cfg=None):
        self.user = user
        self.setup_cfg = setup_cfg

    
    def connect(self) -> sqlite3.Connection:
        try:
            connection_object = sqlite3.connect(
                f"{self.setup_cfg.db_path}{self.setup_cfg.db_name}"
            )
            return connection_object

        except Exception as db_connect_error:
            exception_process.log_error(db_connect_error)


    def create_users_table(self, con_obj) -> bool:
        try:
            con_obj.cursor().execute(
                prt.sql_statement(self.create_users_table.__name__)
            )
            return True
        except Exception as create_users_table_error:
            exception_process.log_error(create_users_table_error)
            return False


    def create_events_table(self, con_obj) -> bool:
        try:
            con_obj.cursor().execute(
                prt.sql_statement(self.create_events_table.__name__)
            )
            return True
        except Exception as create_events_table_error:
            exception_process.log_error(create_events_table_error)
            return False
