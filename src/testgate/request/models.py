# from typing import List, Optional, TYPE_CHECKING
# from sqlmodel import SQLModel, Field, Relationship
#
#
# class Request(SQLModel, table=True):
#
#     __tablename__ = "request"
#
#     id: Optional[int] = Field(primary_key=True)
#     name: str = Field(default=None, unique=True, nullable=False)
#     type: str = Field(default=None, unique=True, nullable=False)
#     description: str = Field(default=None, unique=False, nullable=True)
    