from pathlib import Path


class PylogsSetup:
    def __init__(
        self, 
        db_name="pylogs.db",
        db_users_table="users",
        db_events_table="events",
        user="user",
        password="",
    ):
        self.db_name = db_name
        self.db_users_table = db_users_table
        self.db_events_table = db_events_table
        self.user = user
        self.password = password

    
    def check_db_exists(self):
        return True if Path(f"pylogs/{self.db_name}").is_file() else False


    



def check_setup() -> bool:
    return True if Path("pylogs/pylogs.db").is_file() else False