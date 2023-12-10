from typing import Optional
from sqlmodel import SQLModel
from pydantic import validator
from datetime import datetime, timedelta
from config import Settings
from src.testgate.auth.crypto.password.library import PasswordHashLibrary
from src.testgate.auth.crypto.password.strategy import ScryptPasswordHashStrategy
from src.testgate.auth.oauth2.token.access import AccessToken
from src.testgate.auth.oauth2.token.refresh import RefreshToken
from src.testgate.auth.crypto.digest.strategy import Blake2bMessageDigestStrategy

settings = Settings()
access_token = AccessToken(Blake2bMessageDigestStrategy())
refresh_token = RefreshToken(Blake2bMessageDigestStrategy())
password_hash_library = PasswordHashLibrary(ScryptPasswordHashStrategy())


class LoginCredentials(SQLModel):
    email: str
    password: str


class LoginResponse(SQLModel):
    email: str
    access_token: Optional[str]
    refresh_token: Optional[str]

    @validator("access_token", pre=True, always=True)
    def generate_access_token(cls, v, values, **kwargs):
        now = datetime.utcnow()
        exp = (
            now + timedelta(minutes=settings.testgate_jwt_access_token_exp_minutes)
        ).timestamp()
        payload = {"exp": exp, "email": values["email"]}
        return access_token.encode(
            payload=payload,
            key=settings.testgate_jwt_access_token_key,
            headers={"alg": settings.testgate_jwt_access_token_alg, "typ": "JWT"},
        )

    @validator("refresh_token", pre=True, always=True)
    def generate_refresh_token(cls, v, values, **kwargs):
        now = datetime.utcnow()
        exp = (
            now + timedelta(days=settings.testgate_jwt_refresh_token_exp_days)
        ).timestamp()
        payload = {"exp": exp, "email": values["email"]}
        return refresh_token.encode(
            payload=payload,
            key=settings.testgate_jwt_refresh_token_key,
            headers={"alg": settings.testgate_jwt_refresh_token_alg, "typ": "JWT"},
        )


class RegisterCredentials(SQLModel):
    firstname: str
    lastname: str
    username: str
    email: str
    password: str

    @validator("password", pre=True, always=True)
    def generate_password_hash(cls, v, values, **kwargs):
        return password_hash_library.encode(v)


class RegisterResponse(SQLModel):
    firstname: str
    lastname: str
    username: str
    email: str
