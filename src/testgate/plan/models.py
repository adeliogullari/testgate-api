from typing import List, Optional, TYPE_CHECKING
from sqlmodel import SQLModel, Field, Relationship
from ..link.models import ProjectPlanLink, PlanSuiteLink
from ..suite.models import Suite

if TYPE_CHECKING:
    from ..project.models import Project


class Plan(SQLModel, table=True):

    __tablename__ = "plan"

    id: Optional[int] = Field(primary_key=True)
    name: str = Field(default=None, unique=True, nullable=False)
    description: str = Field(default=None, unique=False, nullable=True)
    projects: List["Project"] = Relationship(back_populates="plans", link_model=ProjectPlanLink)
    suites: List["Suite"] = Relationship(back_populates="plans", link_model=PlanSuiteLink)


Suite.update_forward_refs()
