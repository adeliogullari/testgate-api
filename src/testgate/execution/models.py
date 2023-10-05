from typing import Optional, TYPE_CHECKING, List
from sqlmodel import SQLModel, Field, Relationship

if TYPE_CHECKING:
    from ..repository.models import Repository
    from ..suite.models import Suite


class Execution(SQLModel, table=True):

    __tablename__ = "execution"

    id: Optional[int] = Field(primary_key=True)
    name: str = Field(default=None, unique=True, nullable=False)
    description: str = Field(default=None, unique=False, nullable=True)
    result: Optional["ExecutionResult"] = Relationship(back_populates="execution", sa_relationship_kwargs={'uselist': False})
    repository_id: Optional[int] = Field(default=None, foreign_key="repository.id")
    repository: Optional["Repository"] = Relationship(back_populates="executions")
    suites: List["Suite"] = Relationship(back_populates="execution")


class ExecutionResult(SQLModel, table=True):

    __tablename__ = "execution_result"

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(default=None, unique=True, nullable=False)
    total: Optional[int] = Field(default=0)
    passed: Optional[int] = Field(default=0)
    failed: Optional[int] = Field(default=0)
    skipped: Optional[int] = Field(default=0)
    execution_id: Optional[int] = Field(default=None, foreign_key="execution.id")
    execution: Optional["Execution"] = Relationship(back_populates="result")
