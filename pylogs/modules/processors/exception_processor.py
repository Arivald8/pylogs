import traceback
from datetime import datetime
from modules.printer_model import Printer

prt = Printer()

class ExceptionProcessor:
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
                prt.message("log_exception")
        except Exception as double_exception:
            prt.double_exceptions(exception, double_exception)


    def format_traceback(self, traceback_stack: list) -> str:
        formatted_string_repr = """"""
        for trace in traceback_stack:
            formatted_string_repr += trace
        return formatted_string_repr