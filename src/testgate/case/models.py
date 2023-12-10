from typing import Optional, TYPE_CHECKING
from sqlmodel import SQLModel, Field, Relationship

if TYPE_CHECKING:
    from src.testgate.suite import Suite


class Case(SQLModel, table=True):
    __tablename__ = "case"

    id: Optional[int] = Field(primary_key=True)
    name: str = Field(default=None, unique=True, nullable=False)
    description: str = Field(default=None, unique=False, nullable=True)
    suite_id: Optional[int] = Field(default=None, foreign_key="suite.id")
    suite: Optional["Suite"] = Relationship(back_populates="cases")
    result: Optional["CaseResult"] = Relationship(
        back_populates="case", sa_relationship_kwargs={"uselist": False}
    )


class CaseResult(SQLModel, table=True):
    __tablename__ = "case_result"

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(default=None, unique=True, nullable=False)
    total: Optional[int] = Field(default=0)
    passed: Optional[int] = Field(default=0)
    failed: Optional[int] = Field(default=0)
    skipped: Optional[int] = Field(default=0)
    case_id: Optional[int] = Field(default=None, foreign_key="case.id")
    case: Optional[Case] = Relationship(back_populates="result")


Case.update_forward_refs()
