import secrets
from .blake2b import Blake2b
from .abstract import MessageDigestStrategy


class Blake2bMessageDigestStrategy(MessageDigestStrategy):

    def __init__(self):
        self.blake2b = Blake2b()

    def encode(self,
               data: str,
               key: str = secrets.token_hex(16),
               salt: str = secrets.token_hex(4)) -> bytes:
        return self.blake2b.encode(data=data, key=key, salt=salt)

    def verify(self,
               data: str,
               key: str,
               encoded_data: bytes) -> bool:
        return self.blake2b.verify(data=data, key=key, encoded_data=encoded_data)
