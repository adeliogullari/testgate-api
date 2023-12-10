from typing import Optional
from sqlmodel import SQLModel


class SuiteResult(SQLModel):
    total: int
    passed: int
    failed: int
    skipped: int


class RetrieveSuiteResponseModel(SQLModel):
    id: int
    name: str


class CreateSuiteRequestModel(SQLModel):
    name: str
    result: Optional[SuiteResult]


class CreateSuiteResponseModel(SQLModel):
    id: str
    name: str
    result: Optional[SuiteResult]


class UpdateSuiteRequestModel(SQLModel):
    name: str
    result: Optional[SuiteResult]


class UpdateSuiteResponseModel(SQLModel):
    id: str
    name: str
    result: Optional[SuiteResult]


class DeleteSuiteResponseModel(SQLModel):
    id: str
    name: str
    result: Optional[SuiteResult]
