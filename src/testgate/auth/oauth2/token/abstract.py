import re
import json
import base64
from typing import Any
from itertools import chain, repeat
from abc import ABC, abstractmethod
from .claims import Payload
from secrets import compare_digest
from src.testgate.auth.crypto.digest.library import MessageDigestLibrary


Base64Segment = r"[A-Za-z0-9+/]{4}"
Base64Padding = r"[A-Za-z0-9+/]{2}(?:==)"
Base64OptionalPadding = r"[A-Za-z0-9+/]{3}="
JsonSegment = r"\s*\{.*?}\s*"


class AuthenticationToken(ABC):
    def __init__(self, algorithm: str):
        self.message_digest_library = MessageDigestLibrary(algorithm=algorithm)

    def _is_valid_base64_encoding(self, string: Any) -> bool:
        base64_pattern = re.compile(
            f"^(?:{Base64Segment})*(?:{Base64Padding}?|{Base64OptionalPadding})?$"
        )
        return base64_pattern.match(string) is not None

    def _is_valid_json_string(self, string: Any) -> bool:
        json_pattern = re.compile(f"^{JsonSegment}$", re.DOTALL)
        return json_pattern.match(string) is not None

    def _safe_b64encode_payload(self, payload: Any) -> bytes:
        return base64.b64encode(
            json.dumps(payload).encode(encoding="utf-8", errors="strict")
        )

    def _safe_b64encode_headers(self, headers: Any) -> bytes:
        return base64.b64encode(
            json.dumps(headers).encode(encoding="utf-8", errors="strict")
        )

    def _safe_b64decode_payload(self, payload: str, validate: bool = True) -> bytes:
        if self._is_valid_base64_encoding(payload):
            return base64.b64decode(payload, validate=validate)
        return base64.b64decode(
            base64.b64encode(payload.encode(encoding="utf-8", errors="strict")),
            validate=validate,
        )

    def _safe_b64decode_headers(self, headers: str, validate: bool = True) -> bytes:
        if self._is_valid_base64_encoding(headers):
            return base64.b64decode(headers, validate=validate)
        return base64.b64decode(
            base64.b64encode(headers.encode(encoding="utf-8", errors="strict")),
            validate=validate,
        )

    def _safe_json_loads_payload(self, payload: str) -> Any:
        if self._is_valid_json_string(payload):
            return json.loads(payload)
        return json.loads("{}")

    def _safe_json_loads_headers(self, headers: str) -> Any:
        if self._is_valid_json_string(headers):
            return json.loads(headers)
        return json.loads("{}")

    @abstractmethod
    def encode(self, payload: Any, key: str, headers: Any) -> str:
        payload = self._safe_b64encode_payload(payload=payload)
        headers = self._safe_b64encode_headers(headers=headers)
        signature = self.message_digest_library.encode(
            data=f"{payload}.{headers}", key=key
        )
        return b".".join([payload, headers, signature]).decode("utf-8")

    @abstractmethod
    def decode(self, token: str) -> tuple[Any, Any, Any]:
        payload, headers, signature, *_ = chain(token.split("."), repeat("{}", 3))
        payload = self._safe_json_loads_payload(
            self._safe_b64decode_payload(payload=payload).decode("utf-8")
        )
        headers = self._safe_json_loads_headers(
            self._safe_b64decode_headers(headers=headers).decode("utf-8")
        )
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
        verified = self.verify(key=key, token=token, iss=iss, sub=sub, aud=aud)
        payload, headers, signature = self.decode(token=token)
        return verified, payload, headers, signature
