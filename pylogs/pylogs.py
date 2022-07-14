from modules.pylogs_setup import PylogsSetup
from modules.processors.db_processor import DbProcessor

def main() -> None:
    setup_cfg = PylogsSetup()
    db_process = DbProcessor(setup_cfg=setup_cfg)
    connection_obj = db_process.connect()

    db_process.create_users_table(connection_obj)
    db_process.create_events_table(connection_obj)
    


if __name__ == "__main__":
    main()