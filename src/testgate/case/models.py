from typing import List, Optional, TYPE_CHECKING
from sqlmodel import SQLModel, Field, Relationship
from ..link.models import SuiteCaseLink

if TYPE_CHECKING:
    from ..suite.models import Suite


class Case(SQLModel, table=True):

    __tablename__ = "case"

    id: Optional[int] = Field(default=None, unique=True, nullable=False, primary_key=True)
    name: str = Field(default=None, unique=True, nullable=False)
    description: str = Field(default=None, unique=False, nullable=True)
    suites: List["Suite"] = Relationship(back_populates="cases", link_model=SuiteCaseLink)
