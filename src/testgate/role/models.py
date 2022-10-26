from typing import List, Optional, TYPE_CHECKING
from sqlmodel import SQLModel, Field, Relationship
from ..permission.models import Permission, RolePermission

if TYPE_CHECKING:
    from ..user.models import User


class Role(SQLModel, table=True):

    __tablename__ = "role"

    id: Optional[int] = Field(primary_key=True)
    name: str = Field(default=None, unique=True)
    users: List["User"] = Relationship(back_populates="role")
    # permissions: List["Permission"] = Relationship(back_populates="roles", link_model=RolePermission)


Permission.update_forward_refs()
