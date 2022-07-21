from getpass import getpass
from hashlib import blake2b
from hmac import compare_digest
from logging import exception
import os

from modules.helpers.printer_model import Printer
from modules.processors.exception_processor import ExceptionProcessor

from cryptography.hazmat.primitives.ciphers import (
    Cipher, algorithms, modes
)

class AuthProcessor:
    def __init__(self,
        username=None, 
        password=None, 
        user=None, 
        printer=Printer(),
        exception_process=ExceptionProcessor(Printer())
    ):
        self.username = username
        self.password = password
        self.user = user
        self.printer = printer
        self.exception_process = exception_process

    
    def generate_secret(self, key:bool=None, iv:bool=None):
        if key is not None:
            return os.urandom(32)
        elif iv is not None:
            return os.urandom(16)
        else:
            return None

    
    def hexdigestizer(self, data, secret_key) -> str:
        return blake2b(
            f'{data}'.encode(),
            digest_size=16,
            key=f'{secret_key}'.encode()
        ).hexdigest()
    

    def encrypt_log(self, secret_key, secret_iv, event_log):
        cipher = Cipher(algorithms.AES(secret_key), modes.CTR(secret_iv))
        encryptor = cipher.encryptor()
        encrypted = [encryptor.update(f"{_}".encode()) for _ in event_log]
        encryptor.finalize()
        return encrypted


    def decrypt_log(self, secret_key, secret_iv, event_log):
        cipher = Cipher(algorithms.AES(secret_key), modes.CTR(secret_iv))
        decryptor = cipher.decryptor()
        decrypted = [decryptor.update(_) for _ in event_log]
        decryptor.finalize()
        return [str(_) for _ in decrypted]


    def get_password(self) -> str:
        """
        Prompts user for a password and a confirmation.
        Checks if both are identical and returns password: str.
        """
        attempts = 3  
        while attempts >= 1:
            password = getpass()
            password_confirmation = getpass(prompt="Password (Again): ")

            if password != password_confirmation:
                attempts -= 1
                self.printer.message("password_mismatch")

                if attempts <= 0:
                    self.printer.message("too_many_attempts")
                    exit()
            else:
                self.password = password
                return password


    def login(self, user_obj, password) -> bool:
        try:
            challenge_pass = self.hexdigestizer(password, user_obj[0])
            return compare_digest(challenge_pass, user_obj[3])
        except Exception as user_obj_fetch_failure:
            self.exception_process.log_error(user_obj_fetch_failure, silent=True)
            return compare_digest(
                self.hexdigestizer(password, ""),
                ""
            )
