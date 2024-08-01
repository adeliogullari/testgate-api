import secrets
from src.testgate.auth.crypto.digest.factory import MessageDigestStrategyFactory


class MessageDigestLibrary:
    def __init__(self, algorithm: str):
        self._strategy = MessageDigestStrategyFactory.create(algorithm=algorithm)

    def encode(
        self,
        data: str,
        key: str = secrets.token_hex(16),
        salt: str = secrets.token_hex(4),
    ) -> bytes:
        return self._strategy.encode(data=data, key=key, salt=salt)

    def verify(self, data: str, key: str, encoded_data: bytes) -> bool:
        return self._strategy.verify(data=data, key=key, encoded_data=encoded_data)
