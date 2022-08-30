class InputProcessor:
    """
    Create a callable instance of an input process.
    Initialized with an empty command, updates 
    depending on user input.
    """
    def __init__(self, exception_processor=None, event=None, commands=None):
        self.event = event
        self.commands = commands
        self.exception_processor = exception_processor

    
    def __call__(self) -> str:
        self.any_input()
        if self.cmd_lookup():
            return self.event
        else:
            self.event = ""


    def any_input(self):
        self.event = input("> ")

    
    def cmd_lookup(self) -> bool:
        try:
            return True if self.event in self.commands else False
        except Exception as command_lookup_error:
            self.exception_processor.log_error(command_lookup_error)
