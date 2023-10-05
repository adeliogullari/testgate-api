from typing import Optional
from sqlmodel import SQLModel


class RetrievePermissionResponse(SQLModel):
    id: int
    name: str


class PermissionQueryParameters(SQLModel):
    offset: Optional[int]
    limit: Optional[int]
    name: str


class CreatePermissionRequest(SQLModel):
    name: str


class CreatePermissionResponse(SQLModel):
    id: str
    name: str


class UpdatePermissionRequest(SQLModel):
    name: str


class UpdatePermissionResponse(SQLModel):
    id: str
    name: str


class DeletePermissionResponse(SQLModel):
    id: str
    name: str
