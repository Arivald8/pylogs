import os
import unittest
import sqlite3

from pylogs.modules.pylogs_setup import PylogsSetup
from pylogs.modules.processors.db_processor import DbProcessor
from pylogs.modules.processors.exception_processor import ExceptionProcessor
from pylogs.modules.printer_model import Printer
from pylogs.modules.user_model import User

"""
Mocking the setup of processes for tests.
Do not change the order of instantiation.
"""

prt = Printer()
exception_process = ExceptionProcessor(prt=prt)

setup_cfg = PylogsSetup(
    db_name="test_pylogs.db",
    exception_process=exception_process
)

user_obj = User(
    username="test_username",
    secret_key="test_key",
    secret_iv="test_iv",
    pass_hash="test_hash"
)

db_process = DbProcessor(
    setup_cfg=setup_cfg,
    exception_process=exception_process,
    prt=prt    
)


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


    def test_database_all_table_fetch(self):
        db_process.create_users_table(self.connection_obj)
        db_process.create_events_table(self.connection_obj)

        self.assertListEqual(
            list1=['users', 'event_logs'],
            list2=db_process.get_tables(self.connection_obj)
        )
    

    def test_database_create_user_method(self):
        db_process.create_users_table(self.connection_obj)
        db_process.create_events_table(self.connection_obj)

        self.assertTrue(
            db_process.create_user(
                self.connection_obj,
                user_obj
            )
        )


    def tearDown(self) -> None:
        os.remove(f"{setup_cfg.db_path}{setup_cfg.db_name}")
        self.connection_obj = None
        return super().tearDown()
