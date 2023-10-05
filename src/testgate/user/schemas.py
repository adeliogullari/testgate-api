from sqlmodel import SQLModel
from pydantic import validator
from hashlib import scrypt, blake2b
from bcrypt import hashpw, gensalt
from jose import jwt
from datetime import datetime
from datetime import timedelta
from typing import Optional, List, Any
from ..role.models import Role
from ..team.models import Team

from .constants import *

from src.testgate.auth.crypto.password.library import PasswordHashLibrary
from src.testgate.auth.crypto.password.strategy import ScryptPasswordHashStrategy
password_pash_library = PasswordHashLibrary(ScryptPasswordHashStrategy())


class UserRequestModel(SQLModel):
    firstname: str
    lastname: str
    username: str
    email: str
    verified: bool
    image: Optional[Any]
    role: Optional[Any]
    team: Optional[Any]

    @validator("role", pre=True, always=True)
    def generate_user_role_name(cls, v, values, **kwargs):
        if v:
            return Role(name=v)

    @validator("team", pre=True, always=True)
    def generate_user_team_name(cls, v, values, **kwargs):
        if v:
            return Team(name=v)


class UserResponseModel(SQLModel):
    firstname: str
    lastname: str
    username: str
    email: str
    verified: bool
    image: str
    role: str | None
    team: str | None

    @validator("role", pre=True, always=True)
    def generate_user_role(cls, v, values, **kwargs):
        if v:
            return v.name

    @validator("team", pre=True, always=True)
    def generate_user_team(cls, v, values, **kwargs):
        if v:
            return v.name


class RetrieveUserResponseModel(UserResponseModel):
    id: int


class RetrieveCurrentUserResponseModel(UserResponseModel):
    id: int


class UserQueryParametersModel(SQLModel):
    offset: Optional[int]
    limit: Optional[int]
    firstname: str
    lastname: str
    username: str
    email: str
    verified: bool
    image: str
    role: Optional[Any]
    team: Optional[Any]


class CreateUserRequestModel(UserRequestModel):
    password: str

    @validator("password", pre=True, always=True)
    def generate_password_hash(cls, v, values, **kwargs):
        return password_pash_library.encode(v)


class CreateUserResponseModel(UserResponseModel):
    id: str


class UpdateUserRequestModel(UserRequestModel):
    pass


class UpdateUserResponseModel(UserResponseModel):
    id: str


class VerifyUserResponseModel(UserResponseModel):
    id: str


class ChangeUserPasswordRequestModel(SQLModel):
    current_password: str
    password: str
    password_confirmation: str

    @validator("password", pre=True, always=True)
    def generate_password_hash(cls, v, values, **kwargs):
        return password_pash_library.encode(v)
        # return hashpw(bytes(v, 'UTF-8'), gensalt())

    @validator("password_confirmation", pre=True, always=True)
    def generate_password_confirmation_hash(cls, v, values, **kwargs):
        return password_pash_library.encode(v)

        # return hashpw(bytes(v, 'UTF-8'), gensalt())


class ChangeUserPasswordResponseModel(UserResponseModel):
    id: str


class DeleteUserResponseModel(UserResponseModel):
    id: str


class AuthenticateUserRequestModel(SQLModel):
    email: str
    password: str


class AuthenticateUserResponseModel(UserResponseModel):
    id: str
    token: Optional[str]

    @validator('token', pre=True, always=True)
    def generate_token(cls, v, values, **kwargs):
        now = datetime.utcnow()
        exp = (now + timedelta(seconds=JWT_TOKEN_EXP)).timestamp()
        email = values.get("email")
        claims = {"exp": exp, "email": email}
        return jwt.encode(claims=claims, key=JWT_TOKEN_KEY, algorithm=JWT_TOKEN_ALGORITHM)
