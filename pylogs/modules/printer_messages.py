messages = {
    "startup_message": """
                         /$$                    
                        | $$                    
      /$$$$$$  /$$   /$$| $$  /$$$$$$   /$$$$$$ 
     /$$__  $$| $$  | $$| $$ /$$__  $$ /$$__  $$
    | $$  \ $$| $$  | $$| $$| $$  \ $$| $$  \ $$
    | $$  | $$| $$  | $$| $$| $$  | $$| $$  | $$
    | $$$$$$$/|  $$$$$$$| $$|  $$$$$$/|  $$$$$$$
    | $$____/  \____  $$|__/ \______/  \____  $$
    | $$       /$$  | $$               /$$  \ $$
    | $$      |  $$$$$$/              |  $$$$$$/
    |__/       \______/                \______/ 
    """,

    "tool_description": """A CLI logging tool - Event and data logger.""",

    "help_message": """For usage and available commands, type -h or --help.""",

    "unknown_command": """Unknown command. Please try again.""",

    "available_commands": """
    --help
    -h                Display this message.

    --record-event
    -re               Record an event.

    --view-event
    -ve               View and event.

    --exit
    -e                Exit the tool.

    """,

    "event_types": """
    -ui               User interaction event.
    -ue               User defined event.
    -si               Staff interaction event.
    -se               Staff defined event.
    -o                Other event.
    """,

    "search_types": """
    -d                dd/mm/yyyy
    -t                Title
    -u                User
    -s                Staff
    -all              View all events
    """,

    "invalid_events": """
    Invalid event selection.

    Valid events:
    """,

    "invalid_search_type":
    """
    Invalid search type.

    Valid types:
    """,

    "saving_event": "Saving event...",

    "event_saved": "Event saved.",

    "unknown_error": """
    Unknown error occured... Please repeat the last action.
    Alternatively, check the error logs in "error_log.txt".
    """,

    "event_not_found":"""
    No events matching your criteria were found.
    """,

    "event_not_found":"""
    No events matching your criteria were found.
   """,

    "too_many_attempts": """
    Too many failed attempts. The program will exit.
    """,

    "password_mismatch": """
    The passwords did not match. Try again.
    """,

    "registration_success": """
    Registration successful, please sign in.
    """,

    "log_exception": """
    =============================================
    The last action caused an exception to occur.
    ---------------------------------------------
    If it already doesn't exist, a file named
    error_log.txt has been created in the
    root directory of pylog.py 
    
    You can review the error log to get more 
    information about the exception.
    ---------------------------------------------
    If you are able to replicate the exception,
    please open an issue at:

    https://github.com/Arivald8/pylog/issues

    In the issue, please include the full log of
    the exception and also the necessary steps
    needed to recreate it.
    =============================================
    """,

    "generate_secret_invalid_arguments": """
    =============================================
    The last action caused an exception to occur.
    ---------------------------------------------
    AuthProcessor.generate_secret can be used to generate
    a secret key or secret IV. 
    
    It accepts two optional bool arguments, but only
    one can be passed to generate_secret:
        
        <key=True> or <iv=True>

    If you're seeing this exception, you most likely provided
    both key=True and iv=True as arguments to generate_secret.

    Please provide only 1 argument.
    ============================================= 
    """
}