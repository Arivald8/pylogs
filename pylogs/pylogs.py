from modules.helpers.pylogs_setup import PylogsSetup
from modules.helpers.user_model import User
from modules.helpers.printer_model import Printer

from modules.processors.db_processor import DbProcessor
from modules.processors.auth_processor import AuthProcessor
from modules.processors.exception_processor import ExceptionProcessor
from modules.processors.menu_processor import Menu

user = User()
prt = Printer()

exception_process = ExceptionProcessor(prt=prt)

setup_cfg = PylogsSetup(exception_process=exception_process)

db_process = DbProcessor(
    setup_cfg=setup_cfg,
    exception_process=exception_process,
    prt=prt
)

auth_process = AuthProcessor(user=user)

menu = Menu(db_process=db_process, auth_process=auth_process)


def main() -> None:
    setup_cfg(db_process, auth_process)
    menu.event_loop()


if __name__ == "__main__":
    main()
