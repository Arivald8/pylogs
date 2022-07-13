import os
import unittest
import sqlite3

from pylogs.modules.pylogs_setup import setup_process


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