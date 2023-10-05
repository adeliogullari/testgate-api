from typing import Optional, TYPE_CHECKING
from sqlmodel import SQLModel, Field, Relationship
from ..execution.models import Execution


class Suite(SQLModel, table=True):

    __tablename__ = "suite"

    id: Optional[int] = Field(primary_key=True)
    name: str = Field(default=None, unique=True, nullable=False)
    description: str = Field(default=None, unique=False, nullable=True)
    result: Optional["SuiteResult"] = Relationship(back_populates="suite", sa_relationship_kwargs={'uselist': False})
    execution_id: Optional[int] = Field(default=None, foreign_key="execution.id")
    execution: Optional["Execution"] = Relationship(back_populates="suites")


class SuiteResult(SQLModel, table=True):

    __tablename__ = "suite_result"

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(default=None, unique=True, nullable=False)
    total: Optional[int] = Field(default=0)
    passed: Optional[int] = Field(default=0)
    failed: Optional[int] = Field(default=0)
    skipped: Optional[int] = Field(default=0)
    suite_id: Optional[int] = Field(default=None, foreign_key="suite.id")
    suite: Optional["Suite"] = Relationship(back_populates="result")
