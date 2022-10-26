from typing import Any, List, Optional
from sqlmodel import SQLModel


class SuiteResult(SQLModel):
    name: str


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
