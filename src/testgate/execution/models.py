from typing import Optional, TYPE_CHECKING, List
from sqlmodel import SQLModel, Field, Relationship
from src.testgate.suite.models import Suite

if TYPE_CHECKING:
    from src.testgate.repository.models import Repository


class Execution(SQLModel, table=True):
    __tablename__ = "execution"

    id: int = Field(primary_key=True)
    name: str = Field(unique=True)
    repository_id: Optional[int] = Field(default=None, foreign_key="repository.id")
    repository: Optional["Repository"] = Relationship(back_populates="executions")
    suites: List[Suite] = Relationship(back_populates="execution")
    result: Optional["ExecutionResult"] = Relationship(
        back_populates="execution", sa_relationship_kwargs={"uselist": False}
    )


class ExecutionResult(SQLModel, table=True):
    __tablename__ = "execution_result"

    id: int = Field(primary_key=True)
    total: Optional[int] = Field(default=0)
    passed: Optional[int] = Field(default=0)
    failed: Optional[int] = Field(default=0)
    skipped: Optional[int] = Field(default=0)
    execution_id: Optional[int] = Field(default=None, foreign_key="execution.id")
    execution: Optional[Execution] = Relationship(back_populates="result")


Suite.update_forward_refs()
Execution.update_forward_refs()
