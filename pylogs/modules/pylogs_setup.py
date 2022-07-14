from pathlib import Path

from .processors.exception_processor import ExceptionProcessor

exception_process = ExceptionProcessor


class PylogsSetup:
    def __init__(
        self,
        db_name="pylogs.db",
        db_path="pylogs/",
        db_users_table="users",
        db_events_table="events",
        user="user",
        password="",

    ):
        self.db_name = db_name
        self.db_path = db_path
        self.db_users_table = db_users_table
        self.db_events_table = db_events_table
        self.user = user
        self.password = password


    def check_db_exists(self) -> bool:
        return True if Path(f"{self.db_path}{self.db_name}").is_file() else False


    def create_db(self) -> bool:
        try:
            Path(f"{self.db_path}{self.db_name}").touch(exist_ok=True)
            return True
        except FileExistsError as database_exists:
            exception_process.log_error(exception=database_exists)
            return False


    def create_tables(self):
        pass
        # db_process.create_tables()

