import os
import unittest
import sqlite3

from pylogs.modules.pylogs_setup import PylogsSetup
from pylogs.modules.processors.db_processor import DbProcessor

setup_cfg = PylogsSetup(db_name="test_pylogs.db")
db_process = DbProcessor(setup_cfg=setup_cfg)



class TestSetupDatabaseCreation(unittest.TestCase):
    def setUp(self) -> None:
        if setup_cfg.check_db_exists():
            os.remove(f"{setup_cfg.db_path}{setup_cfg.db_name}")
        return super().setUp()

    def test_setup_database_creation(self):
        self.assertTrue(setup_cfg.create_db())


    def tearDown(self) -> None:
        if setup_cfg.check_db_exists():
            os.remove(f"{setup_cfg.db_path}{setup_cfg.db_name}")
        return super().tearDown()

class TestSetupTableCreation(unittest.TestCase):
    def setUp(self) -> None:
        if not setup_cfg.check_db_exists():
            setup_cfg.create_db()
            self.connection_obj = db_process.connect()
        return super().setUp()
    
    def test_setup_database_table_creation(self):
        pass


    def tearDown(self) -> None:
        os.remove(f"{setup_cfg.db_path}{setup_cfg.db_name}")
        self.connection_obj = None
        return super().tearDown()


class TestDbProcessor(unittest.TestCase):
    def setUp(self) -> None:
        if not setup_cfg.check_db_exists():
            setup_cfg.create_db()
            self.connection_obj = db_process.connect()
        return super().setUp()


    def test_database_connection_method(self):
        self.assertIsInstance(db_process.connect(), sqlite3.Connection)


    
    def test_database_creating_users_table(self):
        self.assertTrue(db_process.create_users_table(self.connection_obj))
    

    
    def test_database_creating_event_table(self):
        self.assertTrue(db_process.create_events_table(self.connection_obj))
    

    def tearDown(self) -> None:
        os.remove(f"{setup_cfg.db_path}{setup_cfg.db_name}")
        self.connection_obj = None
        return super().tearDown()
