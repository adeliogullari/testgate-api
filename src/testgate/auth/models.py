from __future__ import annotations

from bcrypt import checkpw
from typing import List, Optional
from sqlmodel import SQLModel, Field, Relationship
from ..link.models import UserRoleLink, UserTeamLink
from ..role.models import Role
from ..team.models import Team


class User(SQLModel, table=True):

    __tablename__ = "user"

    id: Optional[int] = Field(primary_key=True)
    firstname: str = Field(default=None, unique=False, nullable=False)
    lastname: str = Field(default=None, unique=False, nullable=False)
    email: str = Field(default=None, unique=True, nullable=False)
    password: str = Field(default=None, unique=False, nullable=False)
    verified: bool = Field(default=False, unique=False, nullable=False)
    roles: List["Role"] = Relationship(back_populates="users", link_model=UserRoleLink)
    teams: List["Team"] = Relationship(back_populates="users", link_model=UserTeamLink)

    def check_password(self, password: str):
        return checkpw(password.encode("UTF-8"), bytes(self.password, encoding="UTF-8"))


Role.update_forward_refs()
Team.update_forward_refs()
