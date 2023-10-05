import json
import base64
import hashlib
import secrets
from hashlib import blake2b
from .abstract import MessageDigestAlgorithm


class Blake2b(MessageDigestAlgorithm):
    """Blake2b is an optimized variant of BLAKE."""

    algorithm = "blake2b"
    digest_size = blake2b.MAX_DIGEST_SIZE

    def __init__(self):
        pass

    def encode(self,
               data: str,
               key: str = secrets.token_hex(16),
               salt: str = secrets.token_hex(4)) -> bytes:
        data_hash = hashlib.blake2b(data.encode('utf-8'),
                                    digest_size=self.digest_size,
                                    key=key.encode('utf-8'),
                                    salt=salt.encode('utf-8')).digest()

        return base64.b64encode(json.dumps({'algorithm': self.algorithm,
                                            'data_hash': base64.b64encode(data_hash).decode('utf-8'),
                                            'salt': salt,
                                            'digest_size': self.digest_size}).encode('utf-8'))

    def decode(self, encoded_data: bytes):
        return super().decode(encoded_data=encoded_data)

    def verify(self, data: str, key: str, encoded_data: bytes):
        return super().verify(data=data, key=key, encoded_data=encoded_data)
