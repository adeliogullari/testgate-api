from sqlmodel import SQLModel


class RetrieveRepositoryResponse(SQLModel):
    id: int
    name: str
    # executions: list[str] | None


class RepositoryQueryParameters(SQLModel):
    offset: int
    limit: int
    name: str
    # executions: list[str] | None


class CreateRepositoryRequest(SQLModel):
    name: str
    # executions: list[str] | None


class CreateRepositoryResponse(SQLModel):
    id: int
    name: str
    # executions: list[str] | None


class UpdateRepositoryRequest(SQLModel):
    name: str
    # executions: list[str] | None


class UpdateRepositoryResponse(SQLModel):
    id: int
    name: str
    # executions: list[str] | None


class DeleteRepositoryResponse(SQLModel):
    id: int
    name: str
    # executions: list[str] | None
