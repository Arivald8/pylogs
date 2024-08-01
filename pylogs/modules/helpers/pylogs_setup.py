from pathlib import Path


class PylogsSetup:
    def __init__(
        self,
        db_name="pylogs.db",
        db_path="",
        db_users_table="users",
        db_events_table="events",
        user="user",
        password="",
        exception_process=None,
        user_model = None,

    ):
        self.db_name = db_name
        self.db_path = db_path
        self.db_users_table = db_users_table
        self.db_events_table = db_events_table
        self.user = user
        self.password = password
        self.exception_process = exception_process
        self.user_model = user_model

    
    def __call__(self, db_process, auth_process):
        if not self.check_db_exists():
            self.create_db()
            self.create_tables(db_process)
            self.create_default_user(db_process, auth_process)


    def check_db_exists(self) -> bool:
        return True if Path(f"{self.db_path}{self.db_name}").is_file() else False


    def create_db(self) -> bool:
        try:
            Path(f"{self.db_path}{self.db_name}").touch(exist_ok=True)
            return True
        except FileExistsError as database_exists:
            self.exception_process.log_error(exception=database_exists)
            return False


    def create_tables(self, db_process):
        db_process.create_users_table(db_process.connect())
        db_process.create_events_table(db_process.connect())

    
    def create_default_user(self, db_process, auth_process):
        secret_key = auth_process.generate_secret(key=True)
        secret_iv = auth_process.generate_secret(iv=True)
        pass_hash = auth_process.hexdigestizer(self.password, secret_key)

        self.user_model.secret_key = secret_key
        self.user_model.secret_iv = secret_iv
        self.user_model.pass_hash = pass_hash
        self.user.username = self.user

        db_process.create_user(
            db_process.connect(),
            self.user_model
        )

