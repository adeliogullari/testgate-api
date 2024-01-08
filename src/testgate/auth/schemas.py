from sqlmodel import SQLModel
from datetime import datetime, timedelta
from pydantic import field_validator, Field, ValidationInfo, EmailStr

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
    email: EmailStr
    access_token: str | None = Field(default=None, validate_default=True, strict=True)
    refresh_token: str | None = Field(default=None, validate_default=True, strict=True)

    @field_validator("access_token")
    def generate_access_token(cls, val: str, info: ValidationInfo) -> str:
        now = datetime.utcnow()
        exp = (
            now + timedelta(minutes=settings.testgate_jwt_access_token_exp_minutes)
        ).timestamp()
        payload = {"exp": exp, "email": info.data["email"]}
        return access_token.encode(
            payload=payload,
            key=settings.testgate_jwt_access_token_key,
            headers={"alg": settings.testgate_jwt_access_token_alg, "typ": "JWT"},
        )

    @field_validator("refresh_token")
    def generate_refresh_token(cls, val: str, info: ValidationInfo) -> str:
        now = datetime.utcnow()
        exp = (
            now + timedelta(days=settings.testgate_jwt_refresh_token_exp_days)
        ).timestamp()
        payload = {"exp": exp, "email": info.data["email"]}
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

    @field_validator("password")
    def generate_password(cls, val: str, info: ValidationInfo) -> bytes:
        return password_hash_library.encode(val)


class RegisterResponse(SQLModel):
    firstname: str
    lastname: str
    username: str
    email: str
