import os
import unittest
import sqlite3

from pylogs.modules.pylogs_setup import PylogsSetup

setup_process = PylogsSetup("test_pylogs.db")


class TestSetupDatabaseCreation(unittest.TestCase):
    def setUp(self) -> None:
        if setup_process.check_db_exists():
            os.remove(f"{setup_process.db_path}{setup_process.db_name}")
        return super().setUp()


    def test_setup_database_creation(self):
        self.assertTrue(setup_process.create_db())


    def tearDown(self) -> None:
        if setup_process.check_db_exists():
            os.remove(f"{setup_process.db_path}{setup_process.db_name}")
        return super().tearDown()


class TestSetupTableCreation(unittest.TestCase):
    def setUp(self) -> None:
        if not setup_process.check_db_exists():
            setup_process.create_db()
        return super().setUp()

    
    def test_setup_database_table_creation(self):
        pass


    def tearDown(self) -> None:
        os.remove(f"{setup_process.db_path}{setup_process.db_name}")
        return super().tearDown()