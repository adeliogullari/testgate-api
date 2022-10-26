from sqlmodel import SQLModel
from pydantic import validator
from bcrypt import hashpw, gensalt
from jose import jwt
from datetime import datetime
from datetime import timedelta
from typing import Optional, List
from ..role.models import Role
from ..team.models import Team

from .constants import *


class UserRequestModel(SQLModel):
    firstname: str
    lastname: str
    email: str
    verified: bool
    roles: List[str]
    teams: List[str]


class UserResponseModel(SQLModel):
    firstname: str
    lastname: str
    email: str
    roles: List[str]
    teams: List[str]

    @validator("roles", pre=True, always=True)
    def generate_user_roles(cls, v, values, **kwargs):
        roles_names: List = [role.name for role in v]
        return roles_names

    @validator("teams", pre=True, always=True)
    def generate_user_teams(cls, v, values, **kwargs):
        teams_names: List = [role.name for role in v]
        return teams_names


class RetrieveUserResponseModel(UserResponseModel):
    id: int
    verified: bool


class RetrieveCurrentUserResponseModel(UserResponseModel):
    id: int
    verified: bool


class SearchUserQueryParametersModel(SQLModel):
    offset: Optional[int]
    limit: Optional[int]
    firstname: Optional[str]
    lastname: Optional[str]
    email: Optional[str]
    roles: Optional[List]
    teams: Optional[List]


class SearchUserResponseModel(UserResponseModel):
    pass


class CreateUserRequestModel(UserRequestModel):
    password: str

    @validator("password", pre=True, always=True)
    def generate_password_hash(cls, v, values, **kwargs):
        return hashpw(bytes(v, 'UTF-8'), gensalt())


class CreateUserResponseModel(UserResponseModel):
    id: str
    verified: bool


class UpdateUserRequestModel(UserRequestModel):
    pass


class UpdateUserResponseModel(UserResponseModel):
    id: str
    verified: bool


class DeleteUserResponseModel(UserResponseModel):
    id: str
    verified: bool


class AuthenticateUserRequestModel(SQLModel):
    email: str
    password: str


class AuthenticateUserResponseModel(UserResponseModel):
    id: str
    verified: bool
    access_token: Optional[str]
    refresh_token: Optional[str]

    @validator("access_token", pre=True, always=True)
    def generate_access_token(cls, v, values, **kwargs):
        now = datetime.utcnow()
        exp = (now + timedelta(seconds=JWT_ACCESS_TOKEN_EXP)).timestamp()
        claims = {"exp": exp, "email": values.get("email")}
        return jwt.encode(claims=claims, key=JWT_ACCESS_TOKEN_KEY, algorithm=JWT_ACCESS_TOKEN_ALG)

    @validator("refresh_token", pre=True, always=True)
    def generate_refresh_token(cls, v, values, **kwargs):
        now = datetime.utcnow()
        exp = (now + timedelta(seconds=JWT_REFRESH_TOKEN_EXP)).timestamp()
        claims = {"exp": exp, "email": values.get("email")}
        return jwt.encode(claims=claims, key=JWT_REFRESH_TOKEN_KEY, algorithm=JWT_REFRESH_TOKEN_ALG)


class VerificationUserRequestModel(SQLModel):
    id: int
    firstname: str
    lastname: str
    email: str
    verified: bool
    roles: List[Role]
    teams: List[Team]
    access_token: Optional[str]
    refresh_token: Optional[str]
