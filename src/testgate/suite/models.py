from typing import List, Optional, TYPE_CHECKING
from sqlmodel import SQLModel, Field, Relationship
from ..link.models import PlanSuiteLink, SuiteCaseLink
from ..case.models import Case

if TYPE_CHECKING:
    from ..plan.models import Plan


class Suite(SQLModel, table=True):

    __tablename__ = "suite"

    id: Optional[int] = Field(primary_key=True)
    name: str = Field(default=None, unique=True, nullable=False)
    description: str = Field(default=None, unique=False, nullable=True)
    plans: List["Plan"] = Relationship(back_populates="suites", link_model=PlanSuiteLink)
    cases: List["Case"] = Relationship(back_populates="suites", link_model=SuiteCaseLink)


Case.update_forward_refs()
