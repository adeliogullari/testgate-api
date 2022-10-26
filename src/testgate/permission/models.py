from __future__ import annotations
from typing import List, Optional, TYPE_CHECKING
from bcrypt import hashpw, gensalt, checkpw
from typing import List, Optional
from sqlmodel import SQLModel, Field, Relationship


if TYPE_CHECKING:
    from ..role.models import Role


class RolePermission(SQLModel, table=True):

    __tablename__ = "role_permission"

    role_id: Optional[int] = Field(default=None, foreign_key="role.id", primary_key=True)
    permission_id: Optional[int] = Field(default=None, foreign_key="permission.id", primary_key=True)


class Permission(SQLModel, table=True):

    __tablename__ = "permission"

    id: Optional[int] = Field(primary_key=True)
    name: str = Field(default=None, unique=True, nullable=False)
    active: bool = Field(default=False, unique=False, nullable=False)
    # roles: List["Role"] = Relationship(back_populates="permissions", link_model=RolePermission)
