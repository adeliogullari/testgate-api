from typing import List, Optional, TYPE_CHECKING
from sqlmodel import SQLModel, Field, Relationship
from ..suite.models import Suite

if TYPE_CHECKING:
    from ..project.models import Project


class Run(SQLModel, table=True):

    __tablename__ = "run"

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(default=None, unique=True, nullable=False)
    result: Optional["RunResult"] = Relationship(back_populates="run", sa_relationship_kwargs={'uselist': False})
    suites: List["Suite"] = Relationship(back_populates="run", sa_relationship_kwargs={'uselist': True})
    project_id: Optional[int] = Field(default=None, foreign_key="project.id")
    project: Optional["Project"] = Relationship(back_populates="runs")


class RunResult(SQLModel, table=True):

    __tablename__ = "run_result"

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(default=None, unique=True, nullable=False)
    total: Optional[int] = Field(default=0)
    passed: Optional[int] = Field(default=0)
    failed: Optional[int] = Field(default=0)
    skipped: Optional[int] = Field(default=0)
    run_id: Optional[int] = Field(default=None, foreign_key="run.id")
    run: Optional["Run"] = Relationship(back_populates="result")


Suite.update_forward_refs()
