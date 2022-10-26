import json
import secrets
from typing import Any
from abc import ABC, abstractmethod


class PasswordHashAlgorithm(ABC):

    @abstractmethod
    def encode(self, password: str, salt: str) -> bytes:
        pass

    @abstractmethod
    def decode(self, encoded_password: bytes) -> Any:
        return json.loads(encoded_password.decode())

    @abstractmethod
    def verify(self, password: str, encoded_password: bytes) -> bool:
        decoded_password = self.decode(encoded_password=encoded_password)

        return secrets.compare_digest(self.encode(password=password,
                                                  salt=decoded_password['salt']), encoded_password)


class PasswordHashStrategy(ABC):

    @abstractmethod
    def encode(self, password: str, salt: str) -> bytes:
        pass

    @abstractmethod
    def verify(self, password: str, encoded_password: bytes) -> bool:
        pass
