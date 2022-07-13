import sqlite3

from modules.pylogs_setup import PylogsSetup

setup_process = PylogsSetup()

class DbProcessor:
    def __init__(self, process_user: tuple):
        self.process_user = process_user

    
    def connect(self) -> sqlite3.Connection:
        try:
            return sqlite3.connect(f"{setup_process.db_path}{setup_process.db_name}")
        except Exception as db_connect_error:
            log_error(db_connect_error)