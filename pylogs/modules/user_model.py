class User:
    def __init__(
        self, 
        username=None, 
        password=None, 
        secret_key=None,
        secret_iv=None,
        pass_hash=None
    ):
        
        self.username = username
        self.password = password
        self.secret_key = secret_key
        self.secret_iv = secret_iv
        self.pass_hash = pass_hash


    def __call__(self):
        return (
            self.username,
            self.password,
            self.secret_key,
            self.secret_iv,
            self.pass_hash
        )


    def authenticate(self):
        pass    