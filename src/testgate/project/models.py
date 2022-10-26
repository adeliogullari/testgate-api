from typing import List, Optional, TYPE_CHECKING
from sqlmodel import SQLModel, Field, Relationship
from ..link.models import TeamProjectLink
# from ..plan.models import Plan
from ..run.models import Run


if TYPE_CHECKING:
    from ..team.models import Team


class Project(SQLModel, table=True):

    __tablename__ = "project"

    id: Optional[int] = Field(default=None, unique=True, nullable=False, primary_key=True)
    name: str = Field(default=None, unique=True, nullable=False)
    teams: List["Team"] = Relationship(back_populates="projects", link_model=TeamProjectLink)
    runs: List["Run"] = Relationship(back_populates="project")
    # plans: List["Plan"] = Relationship(back_populates="projects", link_model=ProjectPlanLink)


Run.update_forward_refs()
