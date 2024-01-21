import json
import base64
from typing import Any
from abc import ABC, abstractmethod
from .claims import Payload
from secrets import compare_digest
from src.testgate.auth.crypto.digest.strategy import (
    Blake2bMessageDigestStrategy,
    MessageDigestStrategy,
)
from src.testgate.auth.crypto.digest.blake2b import Blake2b
from src.testgate.auth.crypto.digest.library import MessageDigestLibrary

blake2b = Blake2b()
message_digest_library = MessageDigestLibrary(Blake2bMessageDigestStrategy())


class AuthenticationToken(ABC):
    def __init__(self, strategy: MessageDigestStrategy):
        self._strategy = strategy

    @property
    def strategy(self) -> MessageDigestStrategy:
        return self._strategy

    @strategy.setter
    def strategy(self, strategy: MessageDigestStrategy) -> None:
        self._strategy = strategy

    def _b64encode_payload(self, payload: Any) -> bytes:
        return base64.b64encode(json.dumps(payload).encode("utf-8"))

    def _b64encode_headers(self, headers: Any) -> bytes:
        return base64.b64encode(json.dumps(headers).encode("utf-8"))

    def _b64decode_payload(self, payload: str) -> Any:
        return json.loads(base64.b64decode(payload))

    def _b64decode_headers(self, headers: str) -> Any:
        return json.loads(base64.b64decode(headers))

    @abstractmethod
    def encode(self, payload: Any, key: str, headers: Any) -> str:
        payload = self._b64encode_payload(payload)
        headers = self._b64encode_headers(headers)
        signature = message_digest_library.encode(data=f"{payload}.{headers}", key=key)
        return b".".join([payload, headers, signature]).decode("utf-8")

    @abstractmethod
    def decode(self, token: str) -> tuple[Any, Any, Any]:
        payload, headers, signature = token.split(".")
        payload = self._b64decode_payload(payload)
        headers = self._b64decode_headers(headers)
        return payload, headers, signature

    @abstractmethod
    def verify(
        self,
        key: str,
        token: str,
        iss: str | None = None,
        sub: str | None = None,
        aud: str | None = None,
    ) -> bool:
        payload, headers, signature = self.decode(token=token)
        token = self.encode(payload=payload, key=key, headers=headers)
        is_payload_verified = Payload(**payload).verify(iss=iss, sub=sub, aud=aud)
        decoded_payload, decoded_headers, decoded_signature = self.decode(token=token)
        is_signature_verified = compare_digest(signature, decoded_signature)
        return is_payload_verified and is_signature_verified

    @abstractmethod
    def verify_and_decode(
        self,
        key: str,
        token: str,
        iss: str | None = None,
        sub: str | None = None,
        aud: str | None = None,
    ) -> tuple[bool, Any, Any, Any]:
        try:
            verified = self.verify(key=key, token=token, iss=iss, sub=sub, aud=aud)
            payload, headers, signature = self.decode(token=token)
            return verified, payload, headers, signature
        except:
            return False, "", "", ""
