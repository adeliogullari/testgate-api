import json
from sqlmodel import Session
from redis.asyncio.client import Redis
from src.testgate.repository.models import Repository
from src.testgate.repository.service import (
    create,
    retrieve_by_id,
    retrieve_by_name,
    retrieve_by_query_parameters,
    update,
    delete,
)

from src.testgate.repository.schemas import (
    CreateRepositoryRequest,
    RepositoryQueryParameters,
    UpdateRepositoryRequest,
)


async def test_create(
    sqlmodel_session: Session, redis_client: Redis, repository_factory
):
    repository = CreateRepositoryRequest(**repository_factory.stub().__dict__)

    created_repository = await create(
        sqlmodel_session=sqlmodel_session,
        redis_client=redis_client,
        repository=repository,
    )

    cached_repository = Repository(
        **json.loads(await redis_client.get(name=f"repository_{created_repository.id}"))
    )

    assert cached_repository.name == repository.name
    assert created_repository.name == repository.name


async def test_retrieve_by_id(
    sqlmodel_session: Session, redis_client: Redis, repository
):
    retrieved_repository = await retrieve_by_id(
        sqlmodel_session=sqlmodel_session,
        redis_client=redis_client,
        repository_id=repository.id,
    )

    cached_repository = Repository(
        **json.loads(await redis_client.get(name=f"repository_{repository.id}"))
    )

    assert cached_repository.id == repository.id
    assert retrieved_repository.id == repository.id


async def test_retrieve_by_name(sqlmodel_session: Session, repository):
    retrieved_repository = await retrieve_by_name(
        sqlmodel_session=sqlmodel_session, repository_name=repository.name
    )

    assert retrieved_repository.name == repository.name


async def test_retrieve_by_query_parameters(sqlmodel_session: Session, repository):
    query_parameters = RepositoryQueryParameters(
        offset=0, limit=1, name=repository.name
    )

    retrieved_repository = await retrieve_by_query_parameters(
        sqlmodel_session=sqlmodel_session, query_parameters=query_parameters
    )

    assert retrieved_repository[0].id == repository.id


async def test_update(
    sqlmodel_session: Session, redis_client: Redis, repository_factory, repository
):
    update_repository = UpdateRepositoryRequest(**repository_factory.stub().__dict__)

    updated_repository = await update(
        sqlmodel_session=sqlmodel_session,
        redis_client=redis_client,
        retrieved_repository=repository,
        repository=update_repository,
    )

    cached_repository = Repository(
        **json.loads(await redis_client.get(name=f"repository_{repository.id}"))
    )

    assert cached_repository.id == repository.id
    assert updated_repository.id == repository.id


async def test_delete(sqlmodel_session: Session, redis_client: Redis, repository):
    deleted_repository = await delete(
        sqlmodel_session=sqlmodel_session,
        redis_client=redis_client,
        retrieved_repository=repository,
    )

    cached_repository = await redis_client.get(name=f"repository_{repository.id}")

    assert cached_repository is None
    assert deleted_repository.id == repository.id


async def test_delete_with_cache(
    sqlmodel_session: Session, redis_client: Redis, repository: Repository
):
    await redis_client.set(
        name=f"repository_{repository.id}", value=repository.model_dump_json()
    )

    deleted_repository = await delete(
        sqlmodel_session=sqlmodel_session,
        redis_client=redis_client,
        retrieved_repository=repository,
    )

    cached_repository = await redis_client.get(name=f"repository_{repository.id}")

    assert cached_repository is None
    assert deleted_repository.id == repository.id
