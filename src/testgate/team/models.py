from typing import List, Optional, TYPE_CHECKING
from sqlmodel import SQLModel, Field, Relationship
from ..link.models import TeamProjectLink
from ..project.models import Project

if TYPE_CHECKING:
    from ..user.models import User


class Team(SQLModel, table=True):

    __tablename__ = "team"

    id: Optional[int] = Field(default=None, unique=True, nullable=False, primary_key=True)
    name: str = Field(default=None, unique=True, nullable=False)
    users: List["User"] = Relationship(back_populates="team")
    projects: List["Project"] = Relationship(back_populates="teams", link_model=TeamProjectLink)


Project.update_forward_refs()
