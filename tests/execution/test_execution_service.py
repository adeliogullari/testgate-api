import json
from sqlmodel import Session
from redis.asyncio.client import Redis
from src.testgate.execution.models import Execution
from tests.execution.conftest import ExecutionFactory
from src.testgate.execution.service import (
    create,
    retrieve_by_id,
    retrieve_by_query_parameters,
    update,
    delete,
)

from src.testgate.execution.schemas import (
    CreateExecutionRequest,
    ExecutionQueryParameters,
    UpdateExecutionRequest,
)


async def test_create(
    sqlmodel_session: Session, redis_client: Redis, execution_factory: ExecutionFactory
) -> None:
    execution = CreateExecutionRequest(**execution_factory.stub().__dict__)

    created_execution = await create(
        sqlmodel_session=sqlmodel_session,
        redis_client=redis_client,
        execution=execution,
    )

    cached_execution = Execution(
        **json.loads(await redis_client.get(name=f"execution_{created_execution.id}"))
    )

    assert cached_execution.name == execution.name
    assert created_execution.name == execution.name


async def test_retrieve_by_id(
    sqlmodel_session: Session, redis_client: Redis, execution: Execution
) -> None:
    retrieved_execution = await retrieve_by_id(
        sqlmodel_session=sqlmodel_session,
        redis_client=redis_client,
        execution_id=execution.id,
    )

    cached_execution = Execution(
        **json.loads(await redis_client.get(name=f"execution_{execution.id}"))
    )

    assert cached_execution.id == execution.id
    assert retrieved_execution.id == execution.id


async def test_retrieve_by_cache(
    sqlmodel_session: Session, redis_client: Redis, execution: Execution
) -> None:
    await redis_client.set(
        name=f"execution_{execution.id}", value=execution.model_dump_json()
    )

    retrieved_execution = await retrieve_by_id(
        sqlmodel_session=sqlmodel_session,
        redis_client=redis_client,
        execution_id=execution.id,
    )

    assert retrieved_execution.id == execution.id


async def test_retrieve_by_query_parameters(
    sqlmodel_session: Session, execution: Execution
) -> None:
    query_parameters = ExecutionQueryParameters(offset=0, limit=1, name=execution.name)

    retrieved_execution = await retrieve_by_query_parameters(
        sqlmodel_session=sqlmodel_session, query_parameters=query_parameters
    )

    assert retrieved_execution[0].id == execution.id


async def test_update(
    sqlmodel_session: Session,
    redis_client: Redis,
    execution_factory: ExecutionFactory,
    execution: Execution,
) -> None:
    update_execution = UpdateExecutionRequest(**execution_factory.stub().__dict__)

    updated_execution = await update(
        sqlmodel_session=sqlmodel_session,
        redis_client=redis_client,
        retrieved_execution=execution,
        execution=update_execution,
    )

    cached_execution = Execution(
        **json.loads(await redis_client.get(name=f"execution_{execution.id}"))
    )

    assert cached_execution.id == execution.id
    assert updated_execution.id == execution.id


async def test_delete(
    sqlmodel_session: Session, redis_client: Redis, execution: Execution
) -> None:
    await redis_client.set(
        name=f"execution_{execution.id}", value=execution.model_dump_json()
    )

    deleted_execution = await delete(
        sqlmodel_session=sqlmodel_session,
        redis_client=redis_client,
        retrieved_execution=execution,
    )

    cached_execution = await redis_client.get(name=f"execution_{execution.id}")

    assert cached_execution is None
    assert deleted_execution.id == execution.id
