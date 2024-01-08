from typing import Optional
from sqlmodel import SQLModel, Field


class UserRepositoryLink(SQLModel, table=True):
    __tablename__ = "user_repository"

    user_id: Optional[int] = Field(
        default=None, foreign_key="user.id", primary_key=True
    )
    repository_id: Optional[int] = Field(
        default=None, foreign_key="repository.id", primary_key=True
    )


class RolePermissionLink(SQLModel, table=True):
    __tablename__ = "role_permission"

    role_id: Optional[int] = Field(
        default=None, foreign_key="role.id", primary_key=True
    )
    permission_id: Optional[int] = Field(
        default=None, foreign_key="permission.id", primary_key=True
    )
