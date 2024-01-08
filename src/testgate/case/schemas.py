from sqlmodel import SQLModel
from src.testgate.case.models import CaseResult


class RetrieveCaseResponseModel(SQLModel):
    id: int
    name: str
    description: str


class CaseQueryParameters(SQLModel):
    offset: int
    limit: int
    name: str


class CreateCaseRequestModel(SQLModel):
    name: str
    description: str
    result: CaseResult


class CreateCaseResponseModel(SQLModel):
    id: int
    name: str
    description: str
    result: CaseResult


class UpdateCaseRequestModel(SQLModel):
    name: str
    description: str
    result: CaseResult


class UpdateCaseResponseModel(SQLModel):
    id: int
    name: str
    description: str
    result: CaseResult


class DeleteCaseResponseModel(SQLModel):
    id: int
    name: str
    description: str
    result: CaseResult
