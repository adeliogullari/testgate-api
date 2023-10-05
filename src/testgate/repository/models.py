from typing import List, Optional, TYPE_CHECKING
from sqlmodel import SQLModel, Field, Relationship

from ..link.models import UserRepositoryLink

if TYPE_CHECKING:
    from ..user.models import User
    from ..execution.models import Execution


class Repository(SQLModel, table=True):

    __tablename__ = "repository"

    id: Optional[int] = Field(primary_key=True)
    name: str = Field(default=None, unique=True)
    users: List["User"] = Relationship(back_populates="repositories", link_model=UserRepositoryLink)
    executions: List["Execution"] = Relationship(back_populates="repository")
