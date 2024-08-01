from sqlmodel import SQLModel
from datetime import datetime, timedelta
from pydantic import field_validator, Field, ValidationInfo, EmailStr

from config import Settings
from src.testgate.auth.crypto.password.library import PasswordHashLibrary
from src.testgate.auth.oauth2.token.access import AccessToken
from src.testgate.auth.oauth2.token.refresh import RefreshToken

settings = Settings()
access_token = AccessToken(algorithm=settings.testgate_jwt_access_token_algorithm)
refresh_token = RefreshToken(algorithm=settings.testgate_jwt_refresh_token_algorithm)
password_hash_library = PasswordHashLibrary(
    algorithm=settings.testgate_password_hash_algorithm
)


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
            now
            + timedelta(minutes=settings.testgate_jwt_access_token_expiration_minutes)
        ).timestamp()
        payload = {"exp": exp, "email": info.data["email"]}
        return access_token.encode(
            payload=payload,
            key=settings.testgate_jwt_access_token_key,
            headers={
                "alg": settings.testgate_jwt_access_token_algorithm,
                "typ": settings.testgate_jwt_access_token_type,
            },
        )

    @field_validator("refresh_token")
    def generate_refresh_token(cls, val: str, info: ValidationInfo) -> str:
        now = datetime.utcnow()
        exp = (
            now + timedelta(days=settings.testgate_jwt_refresh_token_expiration_days)
        ).timestamp()
        payload = {"exp": exp, "email": info.data["email"]}
        return refresh_token.encode(
            payload=payload,
            key=settings.testgate_jwt_refresh_token_key,
            headers={
                "alg": settings.testgate_jwt_refresh_token_algorithm,
                "typ": settings.testgate_jwt_refresh_token_type,
            },
        )


class RegisterCredentials(SQLModel):
    firstname: str
    lastname: str
    username: str
    email: str
    password: str

    @field_validator("password", mode="after", check_fields=True)
    def generate_password(cls, val: str, info: ValidationInfo) -> bytes:
        return password_hash_library.encode(password=val)


class RegisterResponse(SQLModel):
    firstname: str
    lastname: str
    username: str
    email: str
