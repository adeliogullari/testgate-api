from typing import Optional, List
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

    created_permission = Repository()
    created_permission.name = repository.name

    session.add(created_permission)
    session.commit()
    session.refresh(created_permission)

    return created_permission


def retrieve_by_id(*, session: Session, repository_id: int) -> Optional[Repository]:
    """Return a repository object based on the given id."""

    statement = select(Repository).where(Repository.id == repository_id)

    retrieved_permission = session.exec(statement).one_or_none()

    return retrieved_permission


def retrieve_by_name(*, session: Session, repository_name: str) -> Optional[Repository]:
    """Return a repository object based on the given name."""

    statement = select(Repository).where(Repository.name == repository_name)

    retrieved_repository = session.exec(statement).one_or_none()

    return retrieved_repository


def retrieve_by_query_parameters(
    *, session: Session, query_parameters: RepositoryQueryParameters
) -> Optional[List[Repository]]:
    """Return list of repository objects based on the given query parameters."""

    statement = select(Repository)

    for attr, value in query_parameters.dict().items():
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
