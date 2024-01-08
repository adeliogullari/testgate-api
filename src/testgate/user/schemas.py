from sqlmodel import SQLModel
from pydantic import field_validator

from src.testgate.role.models import Role
from src.testgate.repository.models import Repository

from src.testgate.auth.crypto.password.library import PasswordHashLibrary
from src.testgate.auth.crypto.password.strategy import ScryptPasswordHashStrategy

password_pash_library = PasswordHashLibrary(ScryptPasswordHashStrategy())


class UserRequestModel(SQLModel):
    firstname: str | None
    lastname: str | None
    username: str
    email: str
    verified: bool
    image: str | None
    role: str | None = None
    repositories: list[str] | None = None

    @field_validator("role", mode="after", check_fields=True)
    def generate_role(cls, v, values, **kwargs):
        if v:
            return Role(name=v)

    @field_validator("repositories", mode="after", check_fields=True)
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
    repositories: list[str] | None

    @field_validator("role", mode="before", check_fields=True)
    def generate_role(cls, v, values, **kwargs):
        if v:
            return v.name

    @field_validator("repositories", mode="before", check_fields=True)
    def generate_repositories(cls, v, values, **kwargs):
        if v:
            return [repository.name for repository in v]


class RetrieveCurrentUserResponseModel(UserResponseModel):
    id: int


class RetrieveUserResponseModel(UserResponseModel):
    id: int


class UserQueryParametersModel(SQLModel):
    offset: int | None
    limit: int | None
    firstname: str | None
    lastname: str | None
    username: str
    email: str
    verified: bool
    role: str | None = None
    repositories: list[str] | None = None


class CreateUserRequestModel(UserRequestModel):
    password: str

    @field_validator("password", mode="before", check_fields=True)
    def generate_password(cls, v, values, **kwargs):
        return password_pash_library.encode(v)


class CreateUserResponseModel(UserResponseModel):
    id: int


class CreateUserRepositoryResponseModel(SQLModel):
    id: int
    name: str


class CreateUserRepositoryRequestModel(SQLModel):
    name: str


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

    @field_validator("password", mode="before", check_fields=True)
    def generate_password(cls, v, values, **kwargs):
        return password_pash_library.encode(v)

    @field_validator("password_confirmation", mode="before", check_fields=True)
    def generate_password_confirmation(cls, v, values, **kwargs):
        return password_pash_library.encode(v)


class ChangeUserPasswordResponseModel(UserResponseModel):
    id: int


class DeleteCurrentUserResponseModel(SQLModel):
    id: int


class DeleteUserResponseModel(UserResponseModel):
    id: int
