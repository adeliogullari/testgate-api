from typing import Any
from .abstract import AuthenticationToken


class BearerToken(AuthenticationToken):
    def encode(self, payload: dict[str, Any], key: str, headers: dict[str, Any]) -> str:
        return super().encode(payload=payload, key=key, headers=headers)

    def decode(self, token: str) -> Any:
        return super().decode(token=token)

    def verify(
        self,
        key: str,
        token: str,
        iss: str | None = None,
        sub: str | None = None,
        aud: str | None = None,
    ) -> bool:
        return super().verify(key=key, token=token, iss=iss, sub=sub, aud=aud)

    def verify_and_decode(
        self,
        key: str,
        token: str,
        iss: str | None = None,
        sub: str | None = None,
        aud: str | None = None,
    ) -> tuple[bool, Any, Any, Any]:
        return super().verify_and_decode(
            key=key, token=token, iss=iss, sub=sub, aud=aud
        )
