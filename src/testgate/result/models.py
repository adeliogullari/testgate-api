# from typing import List, Optional, TYPE_CHECKING
# from sqlmodel import SQLModel, Field, Relationship, Integer
#
# if TYPE_CHECKING:
#     from ..run.models import Run
#
#
# class Result(SQLModel, table=True):
#
#     __tablename__ = "result"
#
#     id: Optional[int] = Field(default=None, primary_key=True)
#     name: str = Field(default=None, unique=True, nullable=False)
#     total: Optional[int] = Field(default=0)
#     passed: Optional[int] = Field(default=0)
#     failed: Optional[int] = Field(default=0)
#     skipped: Optional[int] = Field(default=0)
#     run_id: Optional[int] = Field(default=None, foreign_key="run.id")
#     run: Optional["Run"] = Relationship(back_populates="results")
