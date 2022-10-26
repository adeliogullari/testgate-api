from typing import List, Optional, TYPE_CHECKING
from sqlmodel import SQLModel, Field, Relationship
from ..link.models import UserRoleLink

if TYPE_CHECKING:
    from ..auth.models import User


class Role(SQLModel, table=True):

    __tablename__ = "role"

    id: Optional[int] = Field(default=None, unique=True, nullable=False, primary_key=True)
    name: str = Field(default=None, unique=True, nullable=False)
    users: List["User"] = Relationship(back_populates="roles", link_model=UserRoleLink)
