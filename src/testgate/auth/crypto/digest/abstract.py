import json
import base64
import secrets
from typing import Any
from abc import ABC, abstractmethod


class MessageDigestAlgorithm(ABC):
    @abstractmethod
    def encode(
        self,
        data: str,
        key: str = secrets.token_hex(16),
        salt: str = secrets.token_hex(4),
    ) -> bytes:
        pass

    @abstractmethod
    def decode(self, encoded_data: bytes) -> Any:
        return json.loads(base64.b64decode(encoded_data).decode("utf-8"))

    @abstractmethod
    def verify(self, data: str, key: str, encoded_data: bytes) -> bool:
        decoded_data = self.decode(encoded_data=encoded_data)

        return secrets.compare_digest(
            self.encode(data=data, key=key, salt=decoded_data["salt"]), encoded_data
        )


class MessageDigestStrategy(ABC):
    @abstractmethod
    def encode(self, data: str, key: str, salt: str) -> bytes:
        pass

    @abstractmethod
    def verify(self, data: str, key: str, encoded_data: bytes) -> bool:
        pass
