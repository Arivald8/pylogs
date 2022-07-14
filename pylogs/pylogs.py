from modules.pylogs_setup import PylogsSetup
from modules.user_model import User
from modules.printer_model import Printer

from modules.processors.db_processor import DbProcessor
from modules.processors.exception_processor import ExceptionProcessor

user = User()
prt = Printer()
exception_process = ExceptionProcessor(prt=prt)
setup_cfg = PylogsSetup(exception_process=exception_process)
db_process = DbProcessor(exception_process=exception_process, prt=prt)


def main() -> None:
    pass


if __name__ == "__main__":
    main()
