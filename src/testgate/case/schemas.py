from typing import Optional
from sqlmodel import SQLModel


class CaseResult(SQLModel):
    total: int
    passed: int
    failed: int
    skipped: int


class RetrieveCaseResponseModel(SQLModel):
    id: int
    name: str
    description: str


class CreateCaseRequestModel(SQLModel):
    name: str
    description: str
    result: Optional[CaseResult]


class CreateCaseResponseModel(SQLModel):
    id: str
    name: str
    description: str
    result: Optional[CaseResult]


class UpdateCaseRequestModel(SQLModel):
    name: str
    description: str
    result: Optional[CaseResult]


class UpdateCaseResponseModel(SQLModel):
    id: str
    name: str
    description: str
    result: Optional[CaseResult]


class DeleteCaseResponseModel(SQLModel):
    id: str
    name: str
    description: str
    result: Optional[CaseResult]
