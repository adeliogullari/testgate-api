from typing import List, TYPE_CHECKING
from sqlmodel import SQLModel, Field, Relationship
from src.testgate.permission.models import Permission
from src.testgate.database.models import RolePermissionLink

if TYPE_CHECKING:
    from ..user.models import User


class Role(SQLModel, table=True):
    __tablename__ = "role"

    id: int = Field(primary_key=True)
    name: str = Field(unique=True)
    users: list["User"] = Relationship(back_populates="role")
    permissions: list[Permission] = Relationship(
        back_populates="roles", link_model=RolePermissionLink
    )


Permission.model_rebuild()
