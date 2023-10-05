import json
import base64
import hashlib
import secrets
from .abstract import PasswordHashAlgorithm


class Scrypt(PasswordHashAlgorithm):
    """Scrypt is a password-based essential derivation function and a proof-of-work consensus hash function."""

    algorithm = "scrypt"
    cost_factor = 2 ** 14
    block_size = 8
    parallelization_factor = 1
    maxmem = 0
    dklen = 64

    def __init__(self):
        pass

    def encode(self,
               password: str,
               salt: str = secrets.token_hex(64)) -> bytes:
        password_hash = hashlib.scrypt(password=password.encode('utf-8'),
                                       salt=salt.encode('utf-8'),
                                       n=self.cost_factor,
                                       r=self.block_size,
                                       p=self.parallelization_factor,
                                       maxmem=self.maxmem,
                                       dklen=self.dklen)

        return base64.b64encode(json.dumps({'algorithm': self.algorithm,
                                            'password_hash': base64.b64encode(password_hash).decode('utf-8'),
                                            'salt': salt,
                                            'cost_factor': self.cost_factor,
                                            'block_size': self.block_size,
                                            'parallelization_factor': self.parallelization_factor,
                                            'maxmem': self.maxmem,
                                            'dklen': self.dklen}).encode('utf-8'))

    def decode(self, encoded_password: bytes):
        return super().decode(encoded_password=encoded_password)

    def verify(self, password: str, encoded_password: bytes):
        return super().verify(password=password, encoded_password=encoded_password)
