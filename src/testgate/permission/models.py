from typing import TYPE_CHECKING
from sqlmodel import SQLModel, Field, Relationship
from src.testgate.database.models import RolePermissionLink

if TYPE_CHECKING:
    from ..role.models import Role


class Permission(SQLModel, table=True):
    __tablename__ = "permission"

    id: int = Field(primary_key=True)
    name: str = Field(unique=True)
    roles: list["Role"] = Relationship(
        back_populates="permissions", link_model=RolePermissionLink
    )
