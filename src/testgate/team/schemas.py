from sqlmodel import SQLModel
from typing import Optional, List
from ..user.models import User
from ..project.models import Project


class RetrieveTeamResponseModel(SQLModel):
    id: int
    name: str
    users: List[User]
    projects: List[Project]


class CreateTeamRequestModel(SQLModel):
    name: str


class CreateTeamResponseModel(SQLModel):
    id: str
    name: str


class UpdateTeamRequestModel(SQLModel):
    name: str


class UpdateTeamResponseModel(SQLModel):
    id: str
    name: str


class DeleteTeamResponseModel(SQLModel):
    id: str
    name: str
