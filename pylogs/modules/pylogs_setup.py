from pathlib import Path


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
            open(f"pylogs/{self.db_name}", 'x').close()
            return True
        except:
            return False


setup_process = PylogsSetup()