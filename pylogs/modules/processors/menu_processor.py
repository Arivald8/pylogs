from getpass import getpass
from sys import exit

from modules.helpers.user_model import User
from modules.helpers.printer_model import Printer

from modules.processors.input_processor import InputProcessor
from modules.processors.event_processor import EventProcessor
from modules.processors.db_processor import DbProcessor
from modules.processors.auth_processor import AuthProcessor
from modules.processors.exception_processor import ExceptionProcessor

class Menu:
    def __init__(
        self,
        user = User(),
        printer = Printer(),
        input_process = InputProcessor(),
        event_process = EventProcessor(),
        db_process = DbProcessor(),
        auth_process = AuthProcessor(),
        exception_process = ExceptionProcessor()
    ):
        
        self.user = user
        self.printer = printer
        self.input_process = input_process
        self.event_process = event_process
        self.db_process = db_process
        self.auth_process = auth_process
        self.exception_process = exception_process

        self.commands = {
            "-h": self.printer.message("available_commands"),
            "--help": self.printer.message("available_commands"),
            "-e": exit,
            "--exit": exit,
            "-re": self.event_process.record_event,
            "-ve": self.event_process.view_event,
        }


    def controller(self, fn_call: tuple):
        """
        Checks which function was called by the user
        and controls the flow of execution.
        """
        pass

    def login_or_register(self):
        valid_options = ["login", "register"]
        attempts = 3
        while attempts >= 1:
            log_or_reg = input("Login or Register? \n> ").lower()
            if log_or_reg in valid_options:
                return log_or_reg
            else:
                attempts -= 1
                self.printer.message("invalid_selection")
        exit()


    def event_loop(self):
        registered = False
        selection = self.login_or_register()
        if selection == "register":
            attempts = 3
            while attempts >= 1:
                username = input("Username: ")
                if self.db_process.check_if_user_exists(
                    self.db_process.connect(),
                    username
                ):
                    self.printer.message("username_exists")
                    attempts -= 1
                else:
                    self.user.username = username
                    self.user.secret_key = self.auth_process.generate_secret(key=True)
                    self.user.secret_iv = self.auth_process.generate_secret(iv=True)

                    self.user.pass_hash = self.auth_process.hexdigestizer(
                        data = self.auth_process.get_password(),
                        secret_key = self.user.secret_key
                    )

                    self.db_process.create_user(self.db_process.connect(), self.user)

                    registered = True

        elif selection == "login":
            registered = True

        if registered is True:
            db_user_obj = self.db_process.get_user_object(
                self.db_process.connect(),
                username
            )
            attempts = 3
            while attempts >= 1:
                if self.auth_process.login(db_user_obj, getpass()):
                    # Once the user logs in, we immediatelly 
                    # asign the creator to the event_process instance. 
                    # This is because multiple processes must know who
                    # the creator is and doing it this way, avoids 
                    # having to define it multiple times.
                    self.event_process.creator = self.user.username

                    self.printer.message("startup_message")
                    self.printer.message("tool_description")
                    self.printer.message("help_message")

                    while True:
                        user_input = self.input_process()
                        if user_input in self.commands:
                            fn_name = self.commands[user_input]()
                            """
                            fn_name -> (function name, column to search, search keyword)
                            """
                            if fn_name is not None:
                                self.controller(fn_name)
                else:
                    attempts -= 1
                    self.printer.message("wrong_credentials")
