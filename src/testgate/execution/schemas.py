from typing import Optional
from sqlmodel import SQLModel


class RetrieveExecutionResponse(SQLModel):
    id: int
    name: str
    result: dict


class ExecutionQueryParameters(SQLModel):
    offset: Optional[int]
    limit: Optional[int]
    name: str


class CreateExecutionRequest(SQLModel):
    name: str
    result: dict


class CreateExecutionResponse(SQLModel):
    id: str
    name: str
    result: dict


class UpdateExecutionRequest(SQLModel):
    name: str
    result: dict


class UpdateExecutionResponse(SQLModel):
    id: str
    name: str
    result: dict


class DeleteExecutionResponse(SQLModel):
    id: str
    name: str
    result: dict
