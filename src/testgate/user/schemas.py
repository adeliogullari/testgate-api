from sqlmodel import SQLModel
from typing import Any
from pydantic import field_validator, model_validator, ValidationInfo

from src.testgate.role.models import Role
from src.testgate.repository.models import Repository

from src.testgate.auth.crypto.password.library import PasswordHashLibrary
from src.testgate.auth.crypto.password.strategy import ScryptPasswordHashStrategy
from src.testgate.user.exceptions import InvalidPasswordConfirmationException

password_hash_library = PasswordHashLibrary(ScryptPasswordHashStrategy())


class UserRequestModel(SQLModel):
    firstname: str | None
    lastname: str | None
    username: str
    email: str
    verified: bool
    image: str | None
    role: Any | None = None
    repositories: Any | None = None

    @field_validator("role", mode="after", check_fields=True)
    def generate_role(cls, val: str, info: ValidationInfo) -> Role | str:
        if val:
            return Role(name=val)
        return val

    @field_validator("repositories", mode="after", check_fields=True)
    def generate_repositories(
        cls, val: list[str], info: ValidationInfo
    ) -> list[Repository] | list[str]:
        if val:
            return [Repository(name=repository) for repository in val]
        return val


class UserResponseModel(SQLModel):
    firstname: str | None
    lastname: str | None
    username: str
    email: str
    verified: bool
    image: str | None
    role: Any | None
    repositories: Any | None

    @field_validator("role", mode="before", check_fields=True)
    def generate_role(cls, val: Role, info: ValidationInfo) -> str | Role:
        if val:
            return val.name
        return val

    @field_validator("repositories", mode="before", check_fields=True)
    def generate_repositories(
        cls, val: list[Repository], info: ValidationInfo
    ) -> list[str] | list[Repository]:
        if val:
            return [repository.name for repository in val]
        return val


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
    role: Any | None = None
    repositories: Any | None = None

    @field_validator("role", mode="after", check_fields=True)
    def generate_role(cls, val: str, info: ValidationInfo) -> Role | str:
        if val:
            return Role(name=val)
        return val

    @field_validator("repositories", mode="after", check_fields=True)
    def generate_repositories(
        cls, val: list[str], info: ValidationInfo
    ) -> list[Repository] | list[str]:
        if val:
            return [Repository(name=repository) for repository in val]
        return val


class CreateUserRequestModel(UserRequestModel):
    password: str

    @field_validator("password", mode="after", check_fields=True)
    def generate_password(cls, val: str, info: ValidationInfo) -> bytes:
        return password_hash_library.encode(val)


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

    @model_validator(mode="after")
    def check_passwords_match(self) -> "ChangeUserPasswordRequestModel":
        if self.password != self.password_confirmation:
            raise InvalidPasswordConfirmationException
        return self

    @field_validator("password", mode="after", check_fields=True)
    def generate_password(cls, val: str, info: ValidationInfo) -> bytes:
        return password_hash_library.encode(val)

    @field_validator("password_confirmation", mode="after", check_fields=True)
    def generate_password_confirmation(cls, val: str, info: ValidationInfo) -> bytes:
        return password_hash_library.encode(val)


class ChangeUserPasswordResponseModel(UserResponseModel):
    id: int


class DeleteCurrentUserResponseModel(SQLModel):
    id: int


class DeleteUserResponseModel(UserResponseModel):
    id: int
