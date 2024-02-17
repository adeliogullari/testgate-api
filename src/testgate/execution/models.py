from typing import TYPE_CHECKING
from sqlmodel import SQLModel, Field, Relationship
from src.testgate.suite.models import Suite

if TYPE_CHECKING:
    from src.testgate.repository.models import Repository


class ExecutionResult(SQLModel, table=True):
    __tablename__ = "execution_result"

    id: int = Field(primary_key=True)
    total: int = Field(default=0)
    passed: int = Field(default=0)
    failed: int = Field(default=0)
    skipped: int = Field(default=0)
    total_time: int = Field(default=0)
    execution_id: int | None = Field(default=None, foreign_key="execution.id")
    execution: "Execution" = Relationship(back_populates="result")


class Execution(SQLModel, table=True):
    __tablename__ = "execution"

    id: int = Field(primary_key=True)
    name: str = Field(unique=True)
    repository_id: int | None = Field(default=None, foreign_key="repository.id")
    repository: "Repository" = Relationship(back_populates="executions")
    suites: list[Suite] = Relationship(back_populates="execution")
    result: ExecutionResult = Relationship(
        back_populates="execution", sa_relationship_kwargs={"uselist": False}
    )


Suite.model_rebuild()
Execution.model_rebuild()
