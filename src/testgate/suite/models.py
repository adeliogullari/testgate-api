from datetime import datetime
from typing import TYPE_CHECKING
from sqlmodel import SQLModel, Field, Relationship
from src.testgate.case.models import Case

if TYPE_CHECKING:
    from src.testgate.execution.models import Execution


class SuiteResult(SQLModel, table=True):
    __tablename__ = "suite_result"

    id: int = Field(primary_key=True)
    total: int = Field(default=0)
    passed: int = Field(default=0)
    failed: int = Field(default=0)
    skipped: int = Field(default=0)
    status: str = Field(default="")
    message: str = Field(default="")
    start_time: datetime = Field(default_factory=datetime.utcnow)
    end_time: datetime = Field(default_factory=datetime.utcnow)
    elapsed_time: int = Field(default=0)
    suite_id: int | None = Field(default=None, foreign_key="suite.id")
    suite: "Suite" = Relationship(back_populates="result")


class Suite(SQLModel, table=True):
    __tablename__ = "suite"

    id: int = Field(primary_key=True)
    name: str | None = Field(default=None)
    description: str | None = Field(default=None)
    execution_id: int | None = Field(default=None, foreign_key="execution.id")
    execution: "Execution" = Relationship(back_populates="suites")
    cases: list[Case] = Relationship(back_populates="suite")
    result: SuiteResult = Relationship(
        back_populates="suite", sa_relationship_kwargs={"uselist": False}
    )


Case.model_rebuild()
Suite.model_rebuild()
