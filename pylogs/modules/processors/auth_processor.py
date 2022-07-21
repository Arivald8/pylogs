from hashlib import blake2b
import os

from cryptography.hazmat.primitives.ciphers import (
    Cipher, algorithms, modes
)

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
