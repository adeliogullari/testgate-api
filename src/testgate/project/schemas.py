from sqlmodel import SQLModel
from typing import Optional, List
from ..user.models import User


class RetrieveProjectResponseModel(SQLModel):
    id: int
    name: str
    # users: List[User]


class CreateProjectRequestModel(SQLModel):
    name: str


class CreateProjectResponseModel(SQLModel):
    id: str
    name: str


class UpdateProjectRequestModel(SQLModel):
    name: str


class UpdateProjectResponseModel(SQLModel):
    name: str


class DeleteProjectResponseModel(SQLModel):
    name: str
