from typing import Any, List, Optional
from sqlmodel import SQLModel


class RunResult(SQLModel):
    name: str


class RetrieveRunResponseModel(SQLModel):
    id: int
    name: str


class CreateRunRequestModel(SQLModel):
    name: str
    result: Optional[RunResult]


class CreateRunResponseModel(SQLModel):
    id: str
    name: str
    result: Optional[RunResult]


class UpdateRunRequestModel(SQLModel):
    name: str
    result: Optional[Any]


class UpdateRunResponseModel(SQLModel):
    id: str
    name: str
    result: Optional[Any]


class DeleteRunResponseModel(SQLModel):
    id: str
    name: str
    result: Optional[Any]
