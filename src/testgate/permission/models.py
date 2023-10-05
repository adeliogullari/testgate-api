from typing import List, Optional, TYPE_CHECKING
from sqlmodel import SQLModel, Field, Relationship

from ..link.models import RolePermissionLink

if TYPE_CHECKING:
    from ..role.models import Role


class Permission(SQLModel, table=True):

    __tablename__ = "permission"

    id: Optional[int] = Field(primary_key=True)
    name: str = Field(default=None, unique=True, nullable=False)
    roles: List["Role"] = Relationship(back_populates="permissions", link_model=RolePermissionLink)
