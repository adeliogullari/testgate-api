from uuid import uuid4
from dataclasses import dataclass, field
from datetime import datetime, timedelta


def default_exp() -> float:
    now = datetime.utcnow()
    return (now + timedelta(seconds=7200)).timestamp()


def default_nbf() -> float:
    now = datetime.utcnow()
    return (now - timedelta(seconds=120)).timestamp()


def default_iat() -> float:
    now = datetime.utcnow()
    return (now - timedelta(seconds=120)).timestamp()


def default_jti() -> str:
    return uuid4().hex


@dataclass
class RegisteredClaims:
    iss: str | None = None
    sub: str | None = None
    aud: str | None = None
    exp: float = field(default_factory=default_exp)
    nbf: float = field(default_factory=default_nbf)
    iat: float = field(default_factory=default_iat)
    jti: str = field(default_factory=default_jti)

    def _verify_iss(self, iss: str | None) -> bool:
        return self.iss == iss

    def _verify_sub(self, sub: str | None) -> bool:
        return self.sub == sub

    def _verify_aud(self, aud: str | None) -> bool:
        return self.aud == aud

    def _verify_exp(self, now: float) -> bool:
        return now < self.exp

    def _verify_nbf(self, now: float) -> bool:
        return self.nbf < now

    def _verify_iat(self, now: float) -> bool:
        return self.iat < now

    def verify(
        self, iss: str | None = None, sub: str | None = None, aud: str | None = None
    ) -> bool:
        now = datetime.utcnow().timestamp()
        print("mehmet")
        verified_iss = self._verify_iss(iss=iss)
        print(verified_iss)
        verified_sub = self._verify_sub(sub=sub)
        print(verified_sub)
        verified_aud = self._verify_aud(aud=aud)
        print(verified_aud)
        verified_exp = self._verify_exp(now=now)
        print(verified_exp)
        verified_nbf = self._verify_nbf(now=now)
        print(verified_nbf)
        verified_iat = self._verify_iat(now=now)
        print(verified_iat)
        return (
            verified_iss
            and verified_sub
            and verified_aud
            and verified_exp
            and verified_nbf
            and verified_iat
        )


@dataclass
class CustomClaims:
    email: str | None = None


@dataclass
class PublicClaims:
    auth_time: float | None = None
    acr: float | None = None
    nonce: float | None = None


@dataclass
class PrivateClaims:
    pass


@dataclass
class Payload(RegisteredClaims, CustomClaims, PublicClaims, PrivateClaims):
    pass
