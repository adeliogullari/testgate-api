from datetime import datetime
from typing import TYPE_CHECKING
from sqlmodel import SQLModel, Field, Relationship

if TYPE_CHECKING:
    from src.testgate.suite.models import Suite


class CaseResult(SQLModel, table=True):
    __tablename__ = "case_result"

    id: int = Field(primary_key=True)
    total: int = Field(default=0)
    passed: int = Field(default=0)
    failed: int = Field(default=0)
    skipped: int = Field(default=0)
    status: str = Field(default="")
    source: str = Field(default="")
    message: str = Field(default="")
    documentation: str = Field(default="")
    start_time: datetime = Field(default_factory=datetime.utcnow)
    end_time: datetime = Field(default_factory=datetime.utcnow)
    elapsed_time: int = Field(default=0)
    case_id: int | None = Field(default=None, foreign_key="case.id")
    case: "Case" = Relationship(back_populates="result")


class Case(SQLModel, table=True):
    __tablename__ = "case"

    id: int = Field(primary_key=True)
    name: str = Field(default=None)
    description: str = Field(default=None)
    suite_id: int | None = Field(default=None, foreign_key="suite.id")
    suite: "Suite" = Relationship(back_populates="cases")
    result: CaseResult = Relationship(
        back_populates="case", sa_relationship_kwargs={"uselist": False}
    )


Case.model_rebuild()
