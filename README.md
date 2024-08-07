```
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
    
A CLI logging tool - Event and data logger.
```
___

## Usage

You will be prompted to either login or register a user:

```
Login or Register?
>
```
To register a new user, simply type "register" and provide the necessary information, that is a unique username and password:

```
> register

New Username: Foo
Password:
Password (Again):

Registration successful, please sign in.
```

The option to login simply accepts a username and password:

```
Username: Foo
Password:
```
After which you will be greeted with the startup message:

```
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
    
A CLI logging tool - Event and data logger.
For usage and available commands, type -h or --help.
>
```
Following from the prompt on the terminal, -h or --help reveal the available commands:

```
> --help

    --help
    -h                Display this message.

    --record-event
    -re               Record an event.

    --view-event
    -ve               View and event.

    --exit
    -e                Exit the tool.

    
```

All commands are self explanatory. 

`--record-event` or `-re`, provide the user with an option to record an event, whereas `--view-event` or `-ve` allows to query an event from the database.

The interface for adding an event is the following:

```
> -re
Select an event type: 

    -ui               User interaction event.
    -ue               User defined event.
    -si               Staff interaction event.
    -se               Staff defined event.
    -o                Other event.
    
Event: -o
Title: Test event
User: No users involved
Staff: mr.staff
Notes: Remember to remove access to ...
Saving event...
Event saved.
> 
```

To help with filtering specific events when calling `--view-event`, the user must provide an event type, or alternatively select `-o`, which is just a generic "Other event".

Now, let's try to query the event we just created:

```
> -ve
You can search by: 

    -d                dd/mm/yyyy
    -t                Title
    -u                User
    -s                Staff
    -all              View all events
    
What would you like to search by?
> -s
Search keyword: mr.staff

    __________________
    Date: 27/06/2022
    Time: 15:52:31
    __________________
    Title: Test event
    ------------------
    User: No users involved
    Staff: mr.staff
    ------------------
    Notes:
    Remember to remove access to ...
    
> 
```
___

## Docs
You can find an overview of the codebase below. It explains the flow of execution, as well as the structure of the tool. 

pylog takes the approach of utilizing callable class instances. The main idea to understand is that all necessary processor instances are imported into a single file, from which attributes of the instances can be updated. 

Once we're happy with the results of our actions, we simply call the instance to perform its defined main task. Alternatively, we set attributes on a class instance and then simply call its methods or pass it to other instances. 

For example, the `event_process` instance of `EventProcessor()` is defined with a `__call__` dunder method, allowing us to return the following information related to an event:
```
def __call__(self):
        return [
            self.event_date,
            self.event_time,
            self.event_type,
            self.event_data,
            self.event_user,
            self.event_staff,
            self.event_title
        ]
``` 
The above allows us to abstract the calls slightly and makes life easier when passing objects between different instances. 

For example:
```
db_process.add_event(event_process())
```
___
### **pylog.py**
pylog is the main file of the tool. It acts as a controller and contains the main event loop. It imports processors and printers from defined modules. 

Directory structure of pylog:


    ├── modules/
    │   ├──__init__.py 
    │   ├── printers/
    │   │   ├── __init__.py
    │   │   ├── cmds.py
    │   │   └── printers.py
    │   └── processors/
    │       ├── __init__.py
    │       ├── auth_processor.py
    │       ├── db_processor.py
    │       ├── event_processor.py
    │       └── inputprocessor.py
    ├── tester.py
    ├── .gitignore
    ├── pylog.py
    ├── pylogdb.db
    ├── error_log.txt
    ├── README.md
    └── LICENSE

Acting as a controller, pylog contains a dictionary of valid user commands. Each command corresponds to either a class instance method, or to a printer function:

```
commands = {
    "-h": prt.print_help,
    "--help": prt.print_help,
    "-e": exit,
    "--exit": exit,
    "-re": event_process.record_event,
    "-ve": event_process.view_event,
}
```

While processors are defined as object instances, pylog utilizes only functions. 
___
### *`main():`*

`main()` acts as the main event loop of the tool. First, `main()` asks the user for a login or 
register selection. If the user would like to register
an `auth_process.register()` method is called:

```
def main():
    registered = False
    selection = login_or_register()
    if selection == "register":
        if auth_process.register(db_process):
            registered = True
```
If the methods returns True, the `registered` bool is set to True and the next conditional statement executes.

The user has three attempts to login, after which pylog
will exit:

```
    if registered is True:
        attempts = 3
        while attempts >= 1:
            if auth_process.login(db_process, db_process.connect()):
                event_process.creator = db_process.get_user_obj(db_process.connect())[1]
```

Once the user is logged in, `input_process` takes care of parsing user commands and distributing them to the
`controller()`.

If user commands are found within the commands dictionary, a reference copy of the requested method is created and called:

```
        if user_input in commands:
            fn_name = commands[user_input]()
```
Because the commands correspond to class instance methods, some of them are defined with the `__call__` dunder method. We create a reference copy in order to check whether the command should be passed to the controller function:
```
            if fn_name is not None:
                controller(fn_name)
```
___
### *`controller(fn_call: tuple):`*
`controller(fn_call: tuple)` does not return anything, but rather checks which method was called by the user and controls its flow of execution. 

The controller function must first check if the supplied argument is a tuple:
```
def controller(fn_call: tuple):
    if isinstance(fn_call, tuple):
```
If returned from the `view_event` method, our tuple will have the following structure:
```
fn_call[0] --> Function name
fn_call[1] --> DB column to search
fn_call[2] --> Search keyword
```
If the argument is indeed at tuple, we check for the name of the function within the first element:
```
def controller(fn_call: tuple):
    if isinstance(fn_call, tuple):
        if fn_call[0] == "view_event":
```
For each function name, the resulting action will be different, therefore we define the actions directly within the controller.
If the function name corresponds to the `view_event` method, we utilize the `db_process` instance and its method:

```
       if fn_call[0] == "view_event":
            db_process.view_event(
                search_column=fn_call[1],
                keyword=fn_call[2]
            )
```
If the supplied argument is not a tuple, the controller expects to find a name of the method within the fn_object. For example, the `record_event` method of the `EventProcessor` instance returns its name:
```
return self.record_event.__name__
```
In that case, we utilize the `db_process` instance to call the appropriate action. We also assign the creator of the event. Finally, we catch database exceptions and log them into an `error_log` file:

```
    else:
        if fn_call == "record_event":
            try:
                event_process.creator = db_process.get_user_obj(db_process.connect())[1]

                db_process.add_event(event_process(), db_process.connect())

                prt.print_event_saved()
            except Exception as db_exception:
                log_error(db_exception)
```
This would be all for pylog.py. The rest of the logic is abstracted away within processors and printers. 
___
### **event_processor.py**
`EvenProcessor` class instantiates objects with `event_types` and `search_types` as class variables:

```
class EventProcessor:
    event_types = {
        "-ui": "user-interaction",
        "-ue": "user-event",
        "-si": "staff-interaction",
        "-se": "staff-event",
        "-o": "other",
    }

    search_types = {
        "-d": "date",
        "-t": "event_title",
        "-u": "event_user",
        "-s": "event_staff",
        "-all": "event_all",
    }
```
For instance variables, the following are accessible:
```
    def __init__(
        self,
        event_type="",
        event_date="",
        event_time="",
        event_data="",
        event_user="",
        event_staff="",
        event_title="",
        event_types=event_types,
        search_types=search_types,
    ):
```
As mentioned at the beginning, `event_process` instance is callabe. It returns information about the event itself:
```
    def __call__(self):
        return [
            self.event_date,
            self.event_time,
            self.event_type,
            self.event_data,
            self.event_user,
            self.event_staff,
            self.event_title
        ]
```
There are only two menthods which the `event_process` can access. Those are `record_event` and `view_event`, which are pretty self explanatory. 
___

### *`record_event(self):`*
`record_event` is an abstraction companion to the main event loop of `pylog.py`, `DbProcessor` and `InputProcessor` instances. As the name suggest, it simply records information about a given event and stores in temporarily in memory. 

```
    def record_event(self):
        prt.print_event_types()
        while True:
            event_selection = input("Event: ")
            if event_selection in self.event_types:
                self.event_type = event_selection
                self.event_title = input("Title: ")
                self.event_user = input("User: ")
                self.event_staff = input("Staff: ")
                self.event_data = input("Notes: ")
                break

            elif event_selection in prt.messages["available_commands"]:
                prt.print_invalid_event()
                return False
            else:
                prt.print_unknown()
                return False
```
Additionally, each event record includes a datetime timestamp:

```
self.event_date = datetime.today().strftime("%d/%m/%Y")
self.event_time = datetime.now().strftime("%H:%M:%S")
```

Finally, because the `pylog.py controller` has to distingush between callable methods and other functions, we return the name of the method:

```
return self.record_event.__name__
```
___
### *`view_event(self):`*
Once again, `view_event` is self explanatory. The return value for view_event consists of:

```
Tuple:
    view_event.__name__: str
    self.event_type: str
    search_key: str
```
Just as `record_event` abstract away from `pylog` and `processors`, so does `view_event`. Instead of making database calls directly, it simply structures required information in an `event_process` instance, which is then passed to a `DbProcessor` instance. 

A conditional statement separates two types of event searches. First, it checkes whether the user would like to view all events:

```
if event_selection in self.search_types:
    if event_selection == "-all":
        return(
            self.view_event.__name__,
            self.search_types[event_selection],
            ""
        )
```
In case a user would like to return a specific event, that is covered in the else statement:

```
    else:
        search_key = input("Search keyword: ")
        return (
            self.view_event.__name__,
            self.search_types[event_selection],
            search_key
        )
else:
    prt.print_invalid_search_type()
    continue
```

That is it for `event_processor.py`
___

### **input_processor.py**

`input_processor.py` is a very short Class and instance definition. It features an `InputProcessor` class responsible for `input_process` instances. 

It allows to create a callable instance of an input process. It is initialized with an empty command and updates depending on user input:

```
class InputProcessor:
    def __init__(self, event="", commands=cmds):
        self.event = event
        self.commands = commands

    def __call__(self) -> str:
        self.any_input()
        if self.cmd_lookup():
            return self.event
        else:
            self.event = ""
```

There are two methods of the class - `any_input(self)` and `cmd_lookup(self) -> bool`.

`any_input` is simply a wrapper method over `input()`. It takes user input and sets `self.event` equal to a user command:

```
    def any_input(self):
        user_cmd = input("> ")
        self.event = user_cmd
```
`cmd_lookup` checks if the command exists in available commands and returns a bool:

```
    def cmd_lookup(self) -> bool:
        try:
            return True if self.event in cmds else prt.print_unknown()
        except KeyError:
            prt.print_unknown()
```
___

### **db_processor.py**
`db_processor` is used to abstract the database actions. It makes it easier to work with instances of other processors. 

Currently, there is no option to authenticate, however the `DbProcessor` class takes username and password as instance variables. They will later be used to authenticate users.

Instances of `DbProcessor` have access to 4 methods:

- `connect() -> sqlite3.Connection:`
- `get_user_obj(self,con_obj: sqlite3.Connection)-> tuple:`
-  `add_event(self, event_log: list, con_obj=connect():`
-  `view_event(self, search_column, keyword, con_obj=connect()):`
___
### *`connect():`*
`connect` is a method which returns an sqlite3 cursor object. This object is then passed to other methods within the processor. 

```
try:
    return sqlite3.connect("pylogdb.db")

except Exception as db_connect_error:
    prt.print_unknown_error()
    with open("error_log.txt", "a") as errors:
        errors.write(
            f"""[{datetime.now().strftime(
                '%d/%m/%Y, %H:%M:%S'
            )}] - [{str(db_connect_error)}]\n"""
        )
```
___
### *`get_user_obj(self,con_obj: sqlite3.Connection)-> tuple:`*

`get_user_obj` as the name implies, this method returns a user object tuple -> secret key, username, pass_hash.

```
try:
    user_object = con_obj.cursor().execute("""
        select secret_key, username, pass_hash
        from user
        where username=?""", (self.username,)).fetchone()
    return user_object

except Exception as get_user_error:
    prt.print_unknown_error()
    with open("error_log.txt", "a") as errors:
        errors.write(
            f"""[{datetime.now().strftime(
                '%d/%m/%Y, %H:%M:%S'
            )}] - [{str(get_user_error)}]\n"""
        )
```
___
### *`add_event(self, event_log: list, con_obj=connect())`*

`add_event` processes `event_process` instances:

```
try:
    con_obj.cursor().execute("""
        insert into events values (?, ?, ?, ?, ?, ?, ?)
    """, (
        str(event_log[0]),
        str(event_log[1]),
        str(event_log[2]),
        str(event_log[3]),
        str(event_log[4]),
        str(event_log[5]),
        str(event_log[6])
    ))
    con_obj.commit()
except Exception as e:
    # Below should be changed to use proper logging
    with open("error_log.txt", "a") as errors:
        errors.write(
            f"""[{datetime.now().strftime(
                '%d/%m/%Y, %H:%M:%S'
            )}] - [{str(e)}]\n"""
        )
```
___
### *`view_event(self, search_column, keyword, con_obj=connect())`*

Finally, `view_event` is responsible for fetching events from the database:

```
    def view_event(self, search_column, keyword, con_obj=connect()):
        cur = con_obj.cursor()
        if search_column == "event_all":
            cur.execute(f"""
                select * from events
            """)
            events = cur.fetchall()
        else:
            cur.execute(f"""
                select * from events where {search_column}=?
            """, (keyword,))

            events = cur.fetchall()
        
        if len(events) <= 0:
            prt.print_event_not_found()
        else:
            for event in events:
                prt.print_view_event(event)
```
___