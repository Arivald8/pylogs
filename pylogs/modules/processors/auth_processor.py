import os

class AuthProcessor:
    def __init__(self, username=None, password=None, user=None):
        self.username = username
        self.password = password
        self.user = user

    
    def generate_secret(self, key:bool=None, iv:bool=None):
        if key is not None:
            return os.urandom(32)
        elif iv is not None:
            return os.urandom(16)
        elif key is not None and iv is not None:
            # Invalid arguments passed to this method
            return None
        else:
            # Unknown cause of malfunction
            return None

    