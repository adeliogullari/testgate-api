from sqlmodel import SQLModel
from pydantic import validator
from typing import Optional, List, Any

from src.testgate.role.models import Role
from src.testgate.repository.models import Repository

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
    repositories: Optional[List[Any]]

    @validator("role", pre=True, always=True)
    def generate_role(cls, v, values, **kwargs):
        if v:
            return Role(name=v)

    @validator("repositories", pre=True, always=True)
    def generate_repositories(cls, v, values, **kwargs):
        if v:
            return [Repository(name=repository) for repository in v]


class UserResponseModel(SQLModel):
    firstname: str | None
    lastname: str | None
    username: str
    email: str
    verified: bool
    image: str | None
    role: str | None
    repositories: List[str] | List[None] | None

    @validator("role", pre=True, always=True)
    def generate_role_name(cls, v, values, **kwargs):
        if v:
            return v.name

    @validator("repositories", pre=True, always=True)
    def generate_repositories_name(cls, v, values, **kwargs):
        if v:
            return [repository.name for repository in v]


class RetrieveUserResponseModel(UserResponseModel):
    id: int


class RetrieveCurrentUserResponseModel(UserResponseModel):
    id: int


class RetrieveCurrentUserRepositoryResponseModel(SQLModel):
    id: int
    repositories: List[str] | List[None] | None

    @validator("repositories", pre=True, always=True)
    def generate_repositories_name(cls, v, values, **kwargs):
        if v:
            return [repository.name for repository in v]


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
    repositories: Optional[List[Any]]


class CreateUserRequestModel(UserRequestModel):
    password: str

    @validator("password", pre=True, always=True)
    def generate_password_hash(cls, v, values, **kwargs):
        return password_pash_library.encode(v)


class CreateUserResponseModel(UserResponseModel):
    id: int


class UpdateUserRequestModel(UserRequestModel):
    pass


class UpdateUserResponseModel(UserResponseModel):
    id: int


class VerifyUserResponseModel(UserResponseModel):
    id: int


class ChangeUserPasswordRequestModel(SQLModel):
    current_password: str
    password: str
    password_confirmation: str

    @validator("password", pre=True, always=True)
    def generate_password_hash(cls, v, values, **kwargs):
        return password_pash_library.encode(v)

    @validator("password_confirmation", pre=True, always=True)
    def generate_password_confirmation_hash(cls, v, values, **kwargs):
        return password_pash_library.encode(v)


class ChangeUserPasswordResponseModel(UserResponseModel):
    id: int


class DeleteCurrentUserRepositoryResponseModel(SQLModel):
    id: int


class DeleteUserResponseModel(UserResponseModel):
    id: int


class AuthenticateUserRequestModel(SQLModel):
    email: str
    password: str
