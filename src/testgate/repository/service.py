from typing import Optional, List, Any
from sqlmodel import select, Session
from src.testgate.repository.models import Repository
from src.testgate.repository.schemas import (
    CreateRepositoryRequest,
    RepositoryQueryParameters,
    UpdateRepositoryRequest,
)


def create(
    *, session: Session, repository: CreateRepositoryRequest
) -> Optional[Repository]:
    """Creates a new permission object."""

    created_repository = Repository(name=repository.name)

    session.add(created_repository)
    session.commit()
    session.refresh(created_repository)

    return created_repository


def retrieve_by_id(*, session: Session, repository_id: int) -> Optional[Repository]:
    """Return a repository object based on the given id."""

    statement: Any = select(Repository).where(Repository.id == repository_id)

    retrieved_repository = session.exec(statement).one_or_none()

    return retrieved_repository


def retrieve_by_name(*, session: Session, repository_name: str) -> Optional[Repository]:
    """Return a repository object based on the given name."""

    statement: Any = select(Repository).where(Repository.name == repository_name)

    retrieved_repository = session.exec(statement).one_or_none()

    return retrieved_repository


def retrieve_by_query_parameters(
    *, session: Session, query_parameters: RepositoryQueryParameters
) -> Optional[List[Repository]]:
    """Return list of repository objects based on the given query parameters."""

    offset = query_parameters.offset
    limit = query_parameters.limit

    statement: Any = select(Repository).offset(offset).limit(limit)

    for attr, value in query_parameters.model_dump(
        exclude={"offset", "limit", "executions"}
    ).items():
        if value:
            statement = statement.filter(getattr(Repository, attr).like(value))

    retrieved_permissions = session.exec(statement).all()

    return retrieved_permissions


def update(
    *,
    session: Session,
    retrieved_repository: Repository,
    repository: UpdateRepositoryRequest,
) -> Optional[Repository]:
    """Updates an existing repository object."""

    retrieved_repository.name = repository.name
    updated_permission = retrieved_repository

    session.add(updated_permission)
    session.commit()
    session.refresh(updated_permission)

    return updated_permission


def delete(
    *, session: Session, retrieved_repository: Repository
) -> Optional[Repository]:
    """Deletes an existing repository object."""

    session.delete(retrieved_repository)
    session.commit()

    return retrieved_repository
