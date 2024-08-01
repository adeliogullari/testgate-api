import json
from typing import Any, Sequence
from sqlmodel import select, Session
from redis.asyncio.client import Redis
from .models import Role
from .schemas import CreateRoleRequestModel, RoleQueryParameters, UpdateRoleRequestModel


async def create(*, sqlmodel_session: Session, role: CreateRoleRequestModel) -> Role:
    """Creates a new role object."""

    created_role = Role()
    created_role.name = role.name

    sqlmodel_session.add(created_role)
    sqlmodel_session.commit()
    sqlmodel_session.refresh(created_role)

    return created_role


async def retrieve_by_id(
    *, sqlmodel_session: Session, redis_client: Redis, role_id: int
) -> Role | None:
    """Return a role object based on the given id."""
    if cached_role := await redis_client.get(name=f"role_{role_id}"):
        return Role(**json.loads(cached_role))

    await redis_client.get(name=f"role_{role_id}")

    if retrieved_role := sqlmodel_session.exec(
        select(Role).where(Role.id == role_id)
    ).one_or_none():
        await redis_client.set(
            name=f"role_{role_id}",
            value=retrieved_role.model_dump_json(),
        )

    return retrieved_role


async def retrieve_by_name(*, sqlmodel_session: Session, name: str) -> Role:
    """Return a role object based on the given name."""

    statement: Any = select(Role).where(Role.name == name)

    retrieved_role = sqlmodel_session.exec(statement).one_or_none()

    return retrieved_role


async def retrieve_by_query_parameters(
    *, sqlmodel_session: Session, query_parameters: RoleQueryParameters
) -> Sequence[Role]:
    """Return list of role objects based on the given query parameters."""

    offset = query_parameters.offset
    limit = query_parameters.limit

    statement: Any = select(Role).offset(offset).limit(limit)

    for attr, value in query_parameters.model_dump(
        exclude={"offset", "limit"}, exclude_none=True
    ).items():
        statement = statement.filter(getattr(Role, attr).like(value))

    retrieved_roles = sqlmodel_session.exec(statement).all()

    return retrieved_roles


async def update(
    *,
    sqlmodel_session: Session,
    redis_client: Redis,
    retrieved_role: Role,
    role: UpdateRoleRequestModel,
) -> Role:
    """Updates an existing role object."""

    retrieved_role.name = role.name
    updated_role = retrieved_role

    sqlmodel_session.add(updated_role)
    sqlmodel_session.commit()
    sqlmodel_session.refresh(updated_role)

    await redis_client.set(
        name=f"role_{updated_role.id}",
        value=updated_role.model_dump_json(),
    )

    return updated_role


async def delete(
    *, sqlmodel_session: Session, redis_client: Redis, retrieved_role: Role
) -> Role:
    """Deletes an existing role object."""

    sqlmodel_session.delete(retrieved_role)
    sqlmodel_session.commit()

    await redis_client.delete(f"role_{retrieved_role.id}")

    return retrieved_role
