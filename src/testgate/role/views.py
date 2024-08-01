from typing import List, Sequence
from sqlmodel import Session
from fastapi import status, Depends, APIRouter, HTTPException, Query
from redis.asyncio.client import Redis
from .models import Role
from .service import (
    retrieve_by_id,
    retrieve_by_name,
    retrieve_by_query_parameters,
    create,
    update,
    delete,
)
from .schemas import (
    RetrieveRoleResponseModel,
    RoleQueryParameters,
    CreateRoleRequestModel,
    CreateRoleResponseModel,
    UpdateRoleRequestModel,
    UpdateRoleResponseModel,
    DeleteRoleResponseModel,
)
from src.testgate.database.service import get_sqlmodel_session
from src.testgate.cache.service import get_redis_client

router = APIRouter(tags=["roles"])

RoleNotFoundException = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND, detail="A role with that id does not exist"
)

RoleAlreadyExistsException = HTTPException(
    status_code=status.HTTP_409_CONFLICT, detail="A role with that id already exists"
)


@router.get(
    path="/api/v1/role/{role_id}",
    response_model=None,
    status_code=200,
)
async def retrieve_role_by_id(
    *,
    sqlmodel_session: Session = Depends(get_sqlmodel_session),
    redis_client: Redis = Depends(get_redis_client),
    role_id: int,
) -> Role | None:
    """Retrieve role by id."""

    retrieved_role = await retrieve_by_id(
        sqlmodel_session=sqlmodel_session, redis_client=redis_client, role_id=role_id
    )

    if not retrieved_role:
        raise RoleNotFoundException

    return retrieved_role


@router.get(
    path="/api/v1/roles",
    response_model=List[RetrieveRoleResponseModel],
    status_code=200,
)
async def retrieve_role_by_query_parameters(
    *,
    sqlmodel_session: Session = Depends(get_sqlmodel_session),
    offset: int = 0,
    limit: int = Query(default=100, lte=100),
    name: str = Query(default=None),
) -> Sequence[Role] | None:
    """Search role by name."""

    query_parameters = RoleQueryParameters(offset=offset, limit=limit, name=name)

    retrieved_role = await retrieve_by_query_parameters(
        sqlmodel_session=sqlmodel_session, query_parameters=query_parameters
    )

    return retrieved_role


@router.post(
    path="/api/v1/role",
    response_model=CreateRoleResponseModel,
    status_code=201,
)
async def create_role(
    *,
    sqlmodel_session: Session = Depends(get_sqlmodel_session),
    role: CreateRoleRequestModel,
) -> Role | None:
    """Creates role."""

    retrieved_role = await retrieve_by_name(
        sqlmodel_session=sqlmodel_session, name=role.name
    )

    if retrieved_role:
        raise RoleAlreadyExistsException

    created_role = await create(sqlmodel_session=sqlmodel_session, role=role)

    return created_role


@router.put(
    path="/api/v1/role/{role_id}",
    response_model=UpdateRoleResponseModel,
    status_code=200,
)
async def update_role(
    *,
    sqlmodel_session: Session = Depends(get_sqlmodel_session),
    redis_client: Redis = Depends(get_redis_client),
    role_id: int,
    role: UpdateRoleRequestModel,
) -> Role | None:
    """Updates role."""

    retrieved_role = await retrieve_by_id(
        sqlmodel_session=sqlmodel_session, redis_client=redis_client, role_id=role_id
    )

    if not retrieved_role:
        raise RoleNotFoundException

    updated_role = await update(
        sqlmodel_session=sqlmodel_session,
        redis_client=redis_client,
        retrieved_role=retrieved_role,
        role=role,
    )

    return updated_role


@router.delete(
    path="/api/v1/role/{role_id}",
    response_model=DeleteRoleResponseModel,
    status_code=200,
)
async def delete_role(
    *,
    sqlmodel_session: Session = Depends(get_sqlmodel_session),
    redis_client: Redis = Depends(get_redis_client),
    role_id: int,
) -> Role | None:
    """Deletes role."""

    retrieved_role = await retrieve_by_id(
        sqlmodel_session=sqlmodel_session, redis_client=redis_client, role_id=role_id
    )

    if not retrieved_role:
        raise RoleNotFoundException

    deleted_role = await delete(
        sqlmodel_session=sqlmodel_session,
        redis_client=redis_client,
        retrieved_role=retrieved_role,
    )

    return deleted_role
