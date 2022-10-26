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
    name: str


class DeleteRoleResponseModel(SQLModel):
    name: str