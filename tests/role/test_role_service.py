from sqlmodel import Session
from redis.asyncio.client import Redis
from src.testgate.role.models import Role
from tests.role.conftest import RoleFactory
from src.testgate.role.service import (
    create,
    retrieve_by_id,
    retrieve_by_name,
    update,
    delete,
)
from src.testgate.role.schemas import CreateRoleRequestModel, UpdateRoleRequestModel


async def test_create(sqlmodel_session: Session, role_factory: RoleFactory) -> None:
    role = CreateRoleRequestModel(**role_factory.stub().__dict__)

    created_role = await create(sqlmodel_session=sqlmodel_session, role=role)

    assert created_role.name == role.name


async def test_retrieve_by_id(
    sqlmodel_session: Session, redis_client: Redis, role: Role
) -> None:
    retrieved_role = await retrieve_by_id(
        sqlmodel_session=sqlmodel_session, redis_client=redis_client, role_id=role.id
    )

    assert retrieved_role.id == role.id


async def test_retrieve_by_name(sqlmodel_session: Session, role: Role) -> None:
    retrieved_role = await retrieve_by_name(
        sqlmodel_session=sqlmodel_session, name=role.name
    )

    assert retrieved_role.name == role.name


async def test_update(
    sqlmodel_session: Session,
    redis_client: Redis,
    role_factory: RoleFactory,
    role: Role,
) -> None:
    updated_role = await update(
        sqlmodel_session=sqlmodel_session,
        redis_client=redis_client,
        retrieved_role=role,
        role=UpdateRoleRequestModel(**role_factory.stub().__dict__),
    )

    assert updated_role.id == role.id


async def test_delete(
    sqlmodel_session: Session, redis_client: Redis, role: Role
) -> None:
    deleted_role = await delete(
        sqlmodel_session=sqlmodel_session,
        redis_client=redis_client,
        retrieved_role=role,
    )

    assert deleted_role.id == role.id
