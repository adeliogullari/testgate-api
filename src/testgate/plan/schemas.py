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
from ..suite.models import Suite


class RetrievePlanResponseModel(SQLModel):
    id: int
    name: str
    description: str
    suites: List[Suite]


class CreatePlanRequestModel(SQLModel):
    name: str
    description: str


class CreatePlanResponseModel(SQLModel):
    id: str
    name: str
    description: str
    suites: List[Suite]


class UpdatePlanRequestModel(SQLModel):
    name: str
    description: str
    suites: List[Suite]


class UpdatePlanResponseModel(SQLModel):
    id: str
    name: str
    description: str
    suites: List[Suite]


class DeletePlanResponseModel(SQLModel):
    id: str
    name: str
    description: str
    suites: List[Suite]
