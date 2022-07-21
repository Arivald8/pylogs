from .printer_messages import messages, statements

class Printer:
    def __init__(self, messages=messages, statements=statements):
        self.messages = messages
        self.statements = statements

    
    def message(self, msg):
        print(self.messages[msg])

    
    def event(self, event_log):
        print(f"""
        __________________
        Date: {event_log[0]}
        Time: {event_log[1]}
        __________________
        Title: {event_log[6]}
        ------------------
        User: {event_log[4]}
        Staff: {event_log[5]}
        ------------------
        Notes:
        {event_log[3]}
        """)


    def double_exceptions(self, *args):
        print(f"""
        =============================================
        An exception occured during the handling of
        another exception. 

        The exception handler was trying to save
        an exception log into error_log.txt, but it
        encountered a problem trying to save the file.

        If you're not an administrator within your
        domain, you might have to run pylog with
        escalated privileges in order for pylog
        to create an error_log file. Instead of
        saving both exceptions, you can review
        them below.
        ---------------------------------------------

        If you are able to replicate the exception,
        please open an issue at:

        https://github.com/Arivald8/pylog/issues

        In the issue, please include the full log of
        the exception and also the necessary steps
        needed to recreate it.
        ---------------------------------------------

        First in order, the exception which caused
        the exception handler to quit:
        =============================================
        {args[1]}
        =============================================
        Second in order, the original exception:
        =============================================
        {args[0]}
        =============================================
        """)


    def sql_statement(self, statement: str):
        return statements[statement]