from datetime import datetime

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


    def __init__(
        self,
        event_type="",
        event_date="",
        event_time="",
        event_data="",
        event_user="",
        event_staff="",
        event_title="",
        creator="",
        event_types=event_types,
        search_types=search_types,
    ):

        self.event_type = event_type
        self.event_date = event_date
        self.event_time = event_time
        self.event_data = event_data
        self.event_user = event_user
        self.event_staff = event_staff
        self.event_title = event_title
        self.creator = creator
        self.event_types = event_types
        self.search_types = search_types


    def __call__(self):
        return [
            self.event_date,
            self.event_time,
            self.event_type,
            self.event_data,
            self.event_user,
            self.event_staff,
            self.event_title,
            self.creator
        ]


    def record_event(self) -> __name__:
        while True:
            event_selection = input("Event: ")
            if event_selection in self.event_types:
                self.event_type = event_selection
                self.event_title = input("Title: ")
                self.event_user = input("User: ")
                self.event_staff = input("Staff: ")
                self.event_data = input("Notes: ")
                break
            else:
                return False

        self.event_date = datetime.today().strftime("%d/%m/%Y")
        self.event_time = datetime.now().strftime("%H:%M:%S")
        return self.record_event.__name__


    def view_event(self) -> tuple:
        while True:
            event_selection = input("> ")
            if event_selection in self.search_types:
                if event_selection == "-all":
                    return(
                        self.view_event.__name__,
                        self.search_types[event_selection],
                        ""
                    )
                else:
                    search_key = input("Search keyword: ")
                    return(
                        self.view_event.__name__,
                        self.search_types[event_selection],
                        search_key
                    )
            else:
                # Invalid search types
                return(
                    self.view_event.__name__,
                    None,
                    None,
                )
