import json
from typing import Any, Sequence
from sqlmodel import select, Session
from redis.asyncio.client import Redis
from src.testgate.permission.models import Permission
from .schemas import (
    CreatePermissionRequest,
    PermissionQueryParameters,
    UpdatePermissionRequest,
)


async def create(
    *, sqlmodel_session: Session, permission: CreatePermissionRequest
) -> Permission:
    """Creates a new permission object."""

    created_permission = Permission()
    created_permission.name = permission.name

    sqlmodel_session.add(created_permission)
    sqlmodel_session.commit()
    sqlmodel_session.refresh(created_permission)

    return created_permission


async def retrieve_by_id(
    *, sqlmodel_session: Session, redis_client: Redis, permission_id: int
) -> Permission | None:
    """Return a permission object based on the given id."""

    if cached_execution := await redis_client.get(name=f"permission_{permission_id}"):
        return Permission(**json.loads(cached_execution))

    if retrieved_permission := sqlmodel_session.exec(
        select(Permission).where(Permission.id == permission_id)
    ).one_or_none():
        await redis_client.set(
            name=f"permission_{permission_id}",
            value=retrieved_permission.model_dump_json(),
        )

    return retrieved_permission


async def retrieve_by_name(
    *, sqlmodel_session: Session, permission_name: str
) -> Permission:
    """Return a permission object based on the given name."""

    statement: Any = select(Permission).where(Permission.name == permission_name)

    retrieved_permission = sqlmodel_session.exec(statement).one_or_none()

    return retrieved_permission


async def retrieve_by_query_parameters(
    *, sqlmodel_session: Session, query_parameters: PermissionQueryParameters
) -> Sequence[Permission]:
    """Return list of permission objects based on the given query parameters."""

    statement: Any = select(Permission)

    for attr, value in query_parameters.model_dump(exclude={"offset", "limit"}).items():
        if value:
            statement = statement.filter(getattr(Permission, attr).like(value))

    retrieved_permissions = sqlmodel_session.exec(statement).all()

    return retrieved_permissions


async def update(
    *,
    sqlmodel_session: Session,
    retrieved_permission: Permission,
    permission: UpdatePermissionRequest,
) -> Permission:
    """Updates an existing permission object."""

    retrieved_permission.name = permission.name
    updated_permission = retrieved_permission

    sqlmodel_session.add(updated_permission)
    sqlmodel_session.commit()
    sqlmodel_session.refresh(updated_permission)

    return updated_permission


async def delete(
    *, sqlmodel_session: Session, retrieved_permission: Permission
) -> Permission:
    """Deletes an existing permission object."""

    sqlmodel_session.delete(retrieved_permission)
    sqlmodel_session.commit()

    return retrieved_permission
