import json
from sqlmodel import Session
from redis.asyncio import Redis
from src.testgate.case.models import Case
from tests.case.conftest import CaseFactory
from src.testgate.case.schemas import (
    CaseQueryParameters,
    CreateCaseRequestModel,
    UpdateCaseRequestModel,
)
from src.testgate.case.service import (
    create,
    retrieve_by_id,
    retrieve_by_query_parameters,
    update,
    delete,
)


async def test_create(
    sqlmodel_session: Session, redis_client: Redis, case_factory: CaseFactory
) -> None:
    case = CreateCaseRequestModel(**case_factory.stub().__dict__)

    created_case = await create(
        sqlmodel_session=sqlmodel_session, redis_client=redis_client, case=case
    )

    cached_case = Case(
        **json.loads(await redis_client.get(name=f"case_{created_case.id}"))
    )

    assert cached_case.name == case.name
    assert created_case.name == case.name


async def test_retrieve_by_id(
    sqlmodel_session: Session, redis_client: Redis, case: Case
) -> None:
    retrieved_case = await retrieve_by_id(
        sqlmodel_session=sqlmodel_session, redis_client=redis_client, case_id=case.id
    )

    cached_case = Case(**json.loads(await redis_client.get(name=f"case_{case.id}")))

    assert cached_case.id == case.id
    assert retrieved_case.id == case.id


async def test_retrieve_cache_by_id(
    sqlmodel_session: Session, redis_client: Redis, case: Case
) -> None:
    await redis_client.set(name=f"case_{case.id}", value=case.model_dump_json())

    retrieved_case = await retrieve_by_id(
        sqlmodel_session=sqlmodel_session, redis_client=redis_client, case_id=case.id
    )

    assert retrieved_case.id == case.id


async def test_retrieve_by_query_parameters(
    sqlmodel_session: Session, case: Case
) -> None:
    query_parameters = CaseQueryParameters(offset=0, limit=1, name=case.name)

    retrieved_cases = await retrieve_by_query_parameters(
        sqlmodel_session=sqlmodel_session, query_parameters=query_parameters
    )

    assert retrieved_cases[0].id == case.id


async def test_update(
    sqlmodel_session: Session,
    redis_client: Redis,
    case_factory: CaseFactory,
    case: Case,
) -> None:
    update_case = UpdateCaseRequestModel(**case_factory.stub().__dict__)

    updated_case = await update(
        sqlmodel_session=sqlmodel_session,
        redis_client=redis_client,
        retrieved_case=case,
        case=update_case,
    )

    cached_case = Case(**json.loads(await redis_client.get(name=f"case_{case.id}")))

    assert cached_case.id == case.id
    assert updated_case.id == case.id


async def test_delete(
    sqlmodel_session: Session, redis_client: Redis, case: Case
) -> None:
    await redis_client.set(name=f"case_{case.id}", value=case.model_dump_json())

    deleted_case = await delete(
        sqlmodel_session=sqlmodel_session,
        redis_client=redis_client,
        retrieved_case=case,
    )

    cached_case = await redis_client.get(name=f"case_{case.id}")

    assert cached_case is None
    assert deleted_case.id == case.id
