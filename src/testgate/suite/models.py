from typing import Optional, TYPE_CHECKING, List
from sqlmodel import SQLModel, Field, Relationship
from src.testgate.case.models import Case

if TYPE_CHECKING:
    from src.testgate.execution.models import Execution


class Suite(SQLModel, table=True):
    __tablename__ = "suite"

    id: int = Field(primary_key=True)
    name: Optional[str] = Field(default=None)
    description: str = Field(default=None, unique=False, nullable=True)
    execution_id: Optional[int] = Field(default=None, foreign_key="execution.id")
    execution: Optional["Execution"] = Relationship(back_populates="suites")
    cases: List[Case] = Relationship(back_populates="suite")
    result: Optional["SuiteResult"] = Relationship(
        back_populates="suite", sa_relationship_kwargs={"uselist": False}
    )


class SuiteResult(SQLModel, table=True):
    __tablename__ = "suite_result"

    id: int = Field(primary_key=True)
    total: Optional[int] = Field(default=0)
    passed: Optional[int] = Field(default=0)
    failed: Optional[int] = Field(default=0)
    skipped: Optional[int] = Field(default=0)
    suite_id: Optional[int] = Field(default=None, foreign_key="suite.id")
    suite: Optional[Suite] = Relationship(back_populates="result")


Case.update_forward_refs()
Suite.update_forward_refs()
