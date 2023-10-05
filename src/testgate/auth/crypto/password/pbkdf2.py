import json
import base64
import hashlib
import secrets
from .abstract import PasswordHashAlgorithm


class Pbkdf2(PasswordHashAlgorithm):
    """PBKDF2 is a simple cryptographic key derivation function, which is resistant to dictionary attacks and rainbow
    table attacks."""

    algorithm = "pbkdf2"
    hash_name = "sha256"
    iterations = 600000
    dklen = 64

    def __init__(self):
        pass

    def encode(self,
               password: str,
               salt: str = secrets.token_hex(64)) -> bytes:
        password_hash = hashlib.pbkdf2_hmac(hash_name=self.hash_name,
                                            password=password.encode('utf-8'),
                                            salt=salt.encode('utf-8'),
                                            iterations=self.iterations,
                                            dklen=self.dklen)

        return base64.b64encode(json.dumps({'algorithm': self.algorithm,
                                            'hash_name': self.hash_name,
                                            'password_hash': base64.b64encode(password_hash).decode('utf-8'),
                                            'salt': salt,
                                            'iterations': self.iterations,
                                            'dklen': self.dklen}).encode('utf-8'))

    def decode(self, encoded_password: bytes):
        return super().decode(encoded_password=encoded_password)

    def verify(self, password: str, encoded_password: bytes) -> bool:
        return super().verify(password=password, encoded_password=encoded_password)
