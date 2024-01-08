from sqlmodel import SQLModel
from src.testgate.suite.models import SuiteResult


class RetrieveSuiteResponseModel(SQLModel):
    id: int
    name: str


class CreateSuiteRequestModel(SQLModel):
    name: str
    result: SuiteResult


class CreateSuiteResponseModel(SQLModel):
    id: int
    name: str
    result: SuiteResult


class UpdateSuiteRequestModel(SQLModel):
    name: str
    result: SuiteResult


class UpdateSuiteResponseModel(SQLModel):
    id: int
    name: str
    result: SuiteResult


class DeleteSuiteResponseModel(SQLModel):
    id: int
    name: str
    result: SuiteResult
