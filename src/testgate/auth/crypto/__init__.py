import secrets
from src.testgate.auth.crypto.password.abstract import PasswordHashStrategy


class PasswordHashLibrary:

    def __init__(self, strategy: PasswordHashStrategy):
        self._strategy = strategy

    @property
    def strategy(self) -> PasswordHashStrategy:
        return self._strategy

    @strategy.setter
    def strategy(self, strategy):
        self._strategy = strategy

    def encode(self, password: str, salt: str = secrets.token_hex(64)) -> bytes:
        return self._strategy.encode(password=password, salt=salt)

    def verify(self, password: str, encoded_password: bytes) -> bool:
        return self._strategy.verify(password=password, encoded_password=encoded_password)