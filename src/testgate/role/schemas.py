from typing import List
from sqlmodel import SQLModel
from ..user.models import User


class RetrieveRoleResponseModel(SQLModel):
    id: int
    name: str
    users: List[User]


class CreateRoleRequestModel(SQLModel):
    name: str


class CreateRoleResponseModel(SQLModel):
    id: str
    name: str


class UpdateRoleRequestModel(SQLModel):
    name: str


class UpdateRoleResponseModel(SQLModel):
    id: str
    name: str


class DeleteRoleResponseModel(SQLModel):
    id: str
    name: str
