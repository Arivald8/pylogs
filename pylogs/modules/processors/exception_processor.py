import traceback
from datetime import datetime


class ExceptionProcessor:
    """
    Dunder init expects to receive a printer object
    so that it can output exceptions to the user.

    prt: pylogs.modules.printer_model.Printer
    """
    def __init__(self, prt):
        self.prt = prt


    def log_error(self, exception, silent=False) -> None:
        try:
            if not silent:
                with open("error_log.txt", "a") as errors:
                    errors.write(
                        f"""\n[{datetime.now().strftime(
                            '%d/%m/%Y, %H:%M:%S'
                        )}] - \n{exception}\n[{self.format_traceback(
                            traceback.extract_stack().format()
                        )}]\n"""
                    )
                self.prt.message("log_exception")
        except Exception as double_exception:
            self.prt.double_exceptions(exception, double_exception)


    def format_traceback(self, traceback_stack: list) -> str:
        formatted_string_repr = """"""
        for trace in traceback_stack:
            formatted_string_repr += trace
        return formatted_string_repr