import json
from typing import Any, Sequence
from sqlmodel import select, Session
from redis.asyncio.client import Redis
from src.testgate.repository.models import Repository
from src.testgate.repository.schemas import (
    CreateRepositoryRequest,
    RepositoryQueryParameters,
    UpdateRepositoryRequest,
)


async def create(
    *,
    sqlmodel_session: Session,
    redis_client: Redis,
    repository: CreateRepositoryRequest,
) -> Repository:
    """Creates a new repository object."""

    created_repository = Repository(name=repository.name)

    sqlmodel_session.add(created_repository)
    sqlmodel_session.commit()
    sqlmodel_session.refresh(created_repository)

    await redis_client.set(
        name=f"repository_{created_repository.id}",
        value=created_repository.model_dump_json(),
    )

    return created_repository


async def retrieve_by_id(
    *, sqlmodel_session: Session, redis_client: Redis, repository_id: int
) -> Repository | None:
    """Returns a repository object based on the given id."""

    if cached_repository := await redis_client.get(name=f"repository_{repository_id}"):
        return Repository(**json.loads(cached_repository))

    if retrieved_repository := sqlmodel_session.exec(
        select(Repository).where(Repository.id == repository_id)
    ).one_or_none():
        await redis_client.set(
            name=f"repository_{repository_id}",
            value=retrieved_repository.model_dump_json(),
        )

    return retrieved_repository


async def retrieve_by_name(
    *, sqlmodel_session: Session, repository_name: str
) -> Repository:
    """Return a repository object based on the given name."""

    statement: Any = select(Repository).where(Repository.name == repository_name)

    retrieved_repository = sqlmodel_session.exec(statement).one_or_none()

    return retrieved_repository


async def retrieve_by_query_parameters(
    *, sqlmodel_session: Session, query_parameters: RepositoryQueryParameters
) -> Sequence[Repository]:
    """Return list of repository objects based on the given query parameters."""

    offset = query_parameters.offset
    limit = query_parameters.limit

    statement: Any = select(Repository).offset(offset).limit(limit)

    for attr, value in query_parameters.model_dump(
        exclude={"offset", "limit", "executions"}
    ).items():
        if value:
            statement = statement.filter(getattr(Repository, attr).like(value))

    retrieved_permissions = sqlmodel_session.exec(statement).all()

    return retrieved_permissions


async def update(
    *,
    sqlmodel_session: Session,
    redis_client: Redis,
    retrieved_repository: Repository,
    repository: UpdateRepositoryRequest,
) -> Repository:
    """Updates an existing repository object."""

    retrieved_repository.name = repository.name
    updated_repository = retrieved_repository

    sqlmodel_session.add(updated_repository)
    sqlmodel_session.commit()
    sqlmodel_session.refresh(updated_repository)

    await redis_client.set(
        name=f"repository_{updated_repository.id}",
        value=updated_repository.model_dump_json(),
    )

    return updated_repository


async def delete(
    *, sqlmodel_session: Session, redis_client: Redis, retrieved_repository: Repository
) -> Repository:
    """Deletes an existing repository object."""

    sqlmodel_session.delete(retrieved_repository)
    sqlmodel_session.commit()

    await redis_client.delete(f"repository_{retrieved_repository.id}")

    return retrieved_repository
