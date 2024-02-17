from sqlmodel import SQLModel


class RetrievePermissionResponse(SQLModel):
    id: int
    name: str


class PermissionQueryParameters(SQLModel):
    offset: int
    limit: int
    name: str


class CreatePermissionRequest(SQLModel):
    name: str


class CreatePermissionResponse(SQLModel):
    id: int
    name: str


class UpdatePermissionRequest(SQLModel):
    name: str


class UpdatePermissionResponse(SQLModel):
    id: int
    name: str


class DeletePermissionResponse(SQLModel):
    id: int
    name: str
