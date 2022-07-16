from ctypes import sizeof
import os
import unittest
import sqlite3

from pylogs.modules.pylogs_setup import PylogsSetup
from pylogs.modules.processors.db_processor import DbProcessor
from pylogs.modules.processors.auth_processor import AuthProcessor
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

auth_process = AuthProcessor(
    username=setup_cfg.user,
    password=setup_cfg.password,
    user=user_obj
)

test_events = [
    (
        "00/00/00",
        "00:00:00",
        "test_title",
        "tst",
        "test_event_user",
        "test_event_staff",
        "test_event_data",
        "test_creator"
    ),
    (
        "00/00/01",
        "00:00:00",
        "test_title",
        "tst",
        "test_event_user",
        "test_event_staff",
        "test_event_data",
        "test_creator"
    ),
    (
        "00/00/02",
        "00:00:00",
        "test_title",
        "tst",
        "test_event_user",
        "test_event_staff",
        "test_event_data",
        "test_creator"
    ),
    (
        "00/00/03",
        "00:00:00",
        "test_title",
        "tst",
        "test_event_user",
        "test_event_staff",
        "test_event_data",
        "test_creator"
    ),
    (
        "00/00/04",
        "00:00:00",
        "test_title",
        "tst",
        "test_event_user",
        "test_event_staff",
        "test_event_data",
        "test_creator"
    )
]

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
            db_process.create_user(self.connection_obj, user_obj)
        )


    def test_database_check_if_user_exists_method(self):
        db_process.create_users_table(self.connection_obj)
        db_process.create_events_table(self.connection_obj)
        db_process.create_user(self.connection_obj, user_obj)

        self.assertTrue(
            db_process.check_if_user_exists(
                self.connection_obj, 
                user_obj.username
            )
        )


    def test_database_get_user_object(self):
        db_process.create_users_table(self.connection_obj)
        db_process.create_events_table(self.connection_obj)
        db_process.create_user(self.connection_obj, user_obj)
        user_db_obj = db_process.get_user_object(
            self.connection_obj, user_obj.username)

        self.assertTupleEqual(
            user_obj(),
            user_db_obj
        )


    def test_database_add_event_method(self):
        db_process.create_events_table(self.connection_obj)

        self.assertTrue(
            db_process.add_event(
                db_process.connect(),
                [
                    "00/00/00",
                    "00:00:00",
                    "test_title",
                    "tst",
                    "test_event_user",
                    "test_event_staff",
                    "test_event_data",
                    "test_creator"
                ]
            )
        )


    def test_database_view_event_method(self):
        db_process.create_events_table(self.connection_obj)

        for _ in range(5):
            db_process.add_event(
                    db_process.connect(),
                    [
                        f"00/00/0{_}",
                        "00:00:00",
                        "test_title",
                        "tst",
                        "test_event_user",
                        "test_event_staff",
                        "test_event_data",
                        "test_creator"
                    ]
                )

        all_events = db_process.fetch_event(
            self.connection_obj,
            "test_creator",
            "event_all",
            ""
        )

        date_events = db_process.fetch_event(
            self.connection_obj,
            "test_creator",
            "date",
            "00/00/02"
        )

        title_events = db_process.fetch_event(
            self.connection_obj,
            "test_creator",
            "event_title",
            "test_title"
        )

        user_events = db_process.fetch_event(
            self.connection_obj,
            "test_creator",
            "event_user",
            "test_event_user"
        )

        staff_events = db_process.fetch_event(
            self.connection_obj,
            "test_creator",
            "event_staff",
            "test_event_staff"
        )

        self.assertCountEqual(
            all_events,
            test_events
        )

        self.assertListEqual(
            date_events,
            [test_events[2]]
        )

        self.assertListEqual(
            title_events,
            test_events,
        )

        self.assertListEqual(
            user_events,
            test_events,
        )

        self.assertListEqual(
            staff_events,
            test_events,
        )


    def tearDown(self) -> None:
        os.remove(f"{setup_cfg.db_path}{setup_cfg.db_name}")
        self.connection_obj = None
        return super().tearDown()


class TestAuthProcessor(unittest.TestCase):
    def setUp(self) -> None:
        return super().setUp()


    def test_generate_secret_key(self):
        secret = auth_process.generate_secret(key=True)
        self.assertIsInstance(secret, bytes)
        self.assertEqual(len(secret), 32)


    def test_generate_secret_iv(self):
        secret = auth_process.generate_secret(iv=True)
        self.assertIsInstance(secret, bytes)
        self.assertEqual(len(secret), 16)


    def test_hexdigest_output(self):
        hexdigest = auth_process.hexdigestizer(
            data="test_data",
            secret_key=user_obj.secret_key
        )
        self.assertIsInstance(hexdigest, str)
        self.assertEqual(len(hexdigest),  32)


    def test_log_encryption(self):
        secret_key = auth_process.generate_secret(key=True)
        secret_iv = auth_process.generate_secret(iv=True)

        encrypted_log = auth_process.encrypt_log(
            secret_key,
            secret_iv,
            [
                "00/00/00",
                "00:00:00",
                "test_title",
                "tst",
                "test_event_user",
                "test_event_staff",
                "test_event_data",
                user_obj.username
            ]
        )
        self.assertIsInstance(encrypted_log, list)
        self.assertEqual(len(encrypted_log), 8)
        for _ in encrypted_log:
            self.assertIsInstance(_, bytes)
        

    def test_log_decryption(self):
        secret_key = auth_process.generate_secret(key=True)
        secret_iv = auth_process.generate_secret(iv=True)

        encrypted_log = auth_process.encrypt_log(
            secret_key,
            secret_iv,
            [
                "00/00/00",
                "00:00:00",
                "test_title",
                "tst",
                "test_event_user",
                "test_event_staff",
                "test_event_data",
                user_obj.username
            ]
        )

        decrypted_log = auth_process.decrypt_log(
            secret_key,
            secret_iv,
            encrypted_log
        )

        for _ in decrypted_log:
            self.assertIsInstance(_, str)