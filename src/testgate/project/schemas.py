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


class RetrieveWorkspaceResponseModel(SQLModel):
    id: int
    name: str
    users: List[User]


class CreateWorkspaceRequestModel(SQLModel):
    name: str


class CreateWorkspaceResponseModel(SQLModel):
    id: str
    name: str


class UpdateWorkspaceRequestModel(SQLModel):
    name: str


class UpdateWorkspaceResponseModel(SQLModel):
    name: str


class DeleteWorkspaceResponseModel(SQLModel):
    name: str