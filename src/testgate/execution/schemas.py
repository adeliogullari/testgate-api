from sqlmodel import SQLModel
from src.testgate.execution.models import ExecutionResult


class RetrieveExecutionResponse(SQLModel):
    id: int
    name: str
    # result: ExecutionResult


class ExecutionQueryParameters(SQLModel):
    offset: int
    limit: int
    name: str


class CreateExecutionRequest(SQLModel):
    name: str
    result: ExecutionResult


class CreateExecutionResponse(SQLModel):
    id: int
    name: str
    result: ExecutionResult


class UpdateExecutionRequest(SQLModel):
    name: str
    result: ExecutionResult


class UpdateExecutionResponse(SQLModel):
    id: int
    name: str
    result: ExecutionResult


class DeleteExecutionResponse(SQLModel):
    id: int
    name: str
    result: ExecutionResult
