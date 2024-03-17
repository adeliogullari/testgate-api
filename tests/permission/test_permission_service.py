from src.testgate.permission.service import (
    create,
    retrieve_by_id,
    retrieve_by_name,
    retrieve_by_query_parameters,
    update,
    delete,
)

from src.testgate.permission.schemas import (
    CreatePermissionRequest,
    PermissionQueryParameters,
    UpdatePermissionRequest,
)
from sqlmodel import Session
from redis.asyncio.client import Redis


async def test_create(sqlmodel_session: Session, permission_factory):
    permission = CreatePermissionRequest(**permission_factory.stub().__dict__)

    created_permission = await create(
        sqlmodel_session=sqlmodel_session, permission=permission
    )

    assert created_permission.name == permission.name


async def test_retrieve_by_id(
    sqlmodel_session: Session, redis_client: Redis, permission
):
    retrieved_permission = await retrieve_by_id(
        sqlmodel_session=sqlmodel_session,
        redis_client=redis_client,
        permission_id=permission.id,
    )

    assert retrieved_permission.id == permission.id


async def test_retrieve_by_name(sqlmodel_session: Session, permission):
    retrieved_permission = await retrieve_by_name(
        sqlmodel_session=sqlmodel_session, permission_name=permission.name
    )

    assert retrieved_permission.name == permission.name


async def test_retrieve_by_query_parameters(sqlmodel_session: Session, permission):
    query_parameters = PermissionQueryParameters(
        offset=0, limit=1, name=permission.name
    )

    retrieved_permission = await retrieve_by_query_parameters(
        sqlmodel_session=sqlmodel_session, query_parameters=query_parameters
    )

    assert retrieved_permission[0].id == permission.id


async def test_update(sqlmodel_session: Session, permission_factory, permission):
    update_permission = UpdatePermissionRequest(**permission_factory.stub().__dict__)

    updated_permission = await update(
        sqlmodel_session=sqlmodel_session,
        retrieved_permission=permission,
        permission=update_permission,
    )

    assert updated_permission.id == permission.id


async def test_delete(sqlmodel_session: Session, permission):
    deleted_permission = await delete(
        sqlmodel_session=sqlmodel_session, retrieved_permission=permission
    )

    assert deleted_permission.id == permission.id
