from typing import Optional
from sqlmodel import SQLModel


class RetrieveRepositoryResponse(SQLModel):
    id: int
    name: str


class RepositoryQueryParameters(SQLModel):
    offset: Optional[int]
    limit: Optional[int]
    name: str


class CreateRepositoryRequest(SQLModel):
    name: str


class CreateRepositoryResponse(SQLModel):
    id: str
    name: str


class UpdateRepositoryRequest(SQLModel):
    name: str


class UpdateRepositoryResponse(SQLModel):
    id: str
    name: str


class DeleteRepositoryResponse(SQLModel):
    id: str
    name: str
