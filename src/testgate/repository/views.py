from typing import List
from sqlmodel import Session
from fastapi import Query, Depends, APIRouter
from redis.asyncio.client import Redis
from .exceptions import RepositoryNotFoundException, RepositoryAlreadyExistsException
from .models import Repository
from .schemas import (
    RetrieveRepositoryResponse,
    CreateRepositoryRequest,
    CreateRepositoryResponse,
    RepositoryQueryParameters,
    UpdateRepositoryRequest,
    UpdateRepositoryResponse,
    DeleteRepositoryResponse,
)
from .service import (
    create,
    retrieve_by_id,
    retrieve_by_name,
    retrieve_by_query_parameters,
    update,
    delete,
)
from src.testgate.database.service import get_sqlmodel_session, get_redis_client

router = APIRouter(tags=["repositories"])


@router.get(
    path="/api/v1/repositories/{repository_id}",
    response_model=RetrieveRepositoryResponse,
    status_code=200,
)
async def retrieve_repository_by_id(
    *,
    sqlmodel_session: Session = Depends(get_sqlmodel_session),
    redis_client: Redis = Depends(get_redis_client),
    repository_id: int,
) -> Repository | None:
    """Retrieve repository by id."""

    retrieved_repository = await retrieve_by_id(
        sqlmodel_session=sqlmodel_session,
        redis_client=redis_client,
        repository_id=repository_id,
    )

    if not retrieved_repository:
        raise RepositoryNotFoundException

    return retrieved_repository


@router.get(
    path="/api/v1/repositories",
    response_model=List[RetrieveRepositoryResponse],
    status_code=200,
)
async def retrieve_repository_by_query_parameters(
    *,
    sqlmodel_session: Session = Depends(get_sqlmodel_session),
    offset: int = 0,
    limit: int = Query(default=100, lte=100),
    name: str = Query(default=None),
) -> list[Repository] | None:
    """Retrieves repository by query parameters."""

    query_repository = RepositoryQueryParameters(offset=offset, limit=limit, name=name)

    retrieved_repository = await retrieve_by_query_parameters(
        sqlmodel_session=sqlmodel_session, query_parameters=query_repository
    )

    return retrieved_repository


@router.post(
    path="/api/v1/repositories",
    response_model=CreateRepositoryResponse,
    status_code=201,
)
async def create_repository(
    *,
    sqlmodel_session: Session = Depends(get_sqlmodel_session),
    redis_client=Depends(get_redis_client),
    repository: CreateRepositoryRequest,
) -> Repository | None:
    """Creates repository."""

    retrieved_repository = await retrieve_by_name(
        sqlmodel_session=sqlmodel_session, repository_name=repository.name
    )

    if retrieved_repository:
        raise RepositoryAlreadyExistsException

    created_repository = await create(
        sqlmodel_session=sqlmodel_session,
        redis_client=redis_client,
        repository=repository,
    )

    return created_repository


@router.put(
    path="/api/v1/repositories/{repository_id}",
    response_model=UpdateRepositoryResponse,
    status_code=200,
)
async def update_repository(
    *,
    sqlmodel_session: Session = Depends(get_sqlmodel_session),
    redis_client: Redis = Depends(get_redis_client),
    repository_id: int,
    repository: UpdateRepositoryRequest,
) -> Repository | None:
    """Updates repository."""

    retrieved_repository = await retrieve_by_id(
        sqlmodel_session=sqlmodel_session,
        redis_client=redis_client,
        repository_id=repository_id,
    )

    if not retrieved_repository:
        raise RepositoryNotFoundException

    updated_repository = await update(
        sqlmodel_session=sqlmodel_session,
        redis_client=redis_client,
        retrieved_repository=retrieved_repository,
        repository=repository,
    )

    return updated_repository


@router.delete(
    path="/api/v1/repositories/{repository_id}",
    response_model=DeleteRepositoryResponse,
    status_code=200,
)
async def delete_repository(
    *,
    sqlmodel_session: Session = Depends(get_sqlmodel_session),
    redis_client: Redis = Depends(get_redis_client),
    repository_id: int,
) -> Repository | None:
    """Deletes repository."""

    retrieved_repository = await retrieve_by_id(
        sqlmodel_session=sqlmodel_session,
        redis_client=redis_client,
        repository_id=repository_id,
    )

    if not retrieved_repository:
        raise RepositoryNotFoundException

    deleted_repository = await delete(
        sqlmodel_session=sqlmodel_session,
        redis_client=redis_client,
        retrieved_repository=retrieved_repository,
    )

    return deleted_repository
