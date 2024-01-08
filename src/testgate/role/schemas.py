from enum import StrEnum
from sqlmodel import SQLModel
from src.testgate.user.models import User


class Roles(StrEnum):
    DEVELOPER = "Developer"
    ADMINISTRATOR = "Administrator"


class RetrieveRoleResponseModel(SQLModel):
    id: int
    name: str
    users: list[User]


class CreateRoleRequestModel(SQLModel):
    name: str


class CreateRoleResponseModel(SQLModel):
    id: int
    name: str


class UpdateRoleRequestModel(SQLModel):
    name: str


class UpdateRoleResponseModel(SQLModel):
    id: int
    name: str


class DeleteRoleResponseModel(SQLModel):
    id: int
    name: str
