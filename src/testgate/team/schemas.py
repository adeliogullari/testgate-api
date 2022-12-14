from sqlmodel import SQLModel
from pydantic import validator
from bcrypt import hashpw, gensalt
from jose import jwt
from datetime import datetime
from datetime import timedelta
from typing import Optional, List
from ..role.models import Role
from ..team.models import Team
from ..auth.models import User
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
    name: str


class DeleteTeamResponseModel(SQLModel):
    name: str