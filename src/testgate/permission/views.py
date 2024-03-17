from typing import List
from sqlmodel import Session
from redis.asyncio.client import Redis
from fastapi import Query, Depends, APIRouter
from .exceptions import PermissionNotFoundException, PermissionAlreadyExistsException
from .schemas import (
    RetrievePermissionResponse,
    CreatePermissionRequest,
    CreatePermissionResponse,
    PermissionQueryParameters,
    UpdatePermissionRequest,
    UpdatePermissionResponse,
    DeletePermissionResponse,
)
from .models import Permission
from .service import (
    create,
    retrieve_by_id,
    retrieve_by_name,
    retrieve_by_query_parameters,
    update,
    delete,
)
from src.testgate.database.service import get_sqlmodel_session, get_redis_client

router = APIRouter(tags=["permissions"])


@router.get(
    path="/api/v1/permission/{permission_id}",
    response_model=RetrievePermissionResponse,
    status_code=200,
)
async def retrieve_permission_by_id(
    *,
    sqlmodel_session: Session = Depends(get_sqlmodel_session),
    redis_client: Redis = Depends(get_redis_client),
    permission_id: int,
) -> Permission | None:
    """Retrieve permission by id."""

    retrieved_permission = await retrieve_by_id(
        sqlmodel_session=sqlmodel_session,
        redis_client=redis_client,
        permission_id=permission_id,
    )

    if not retrieved_permission:
        raise PermissionNotFoundException

    return retrieved_permission


@router.get(
    path="/api/v1/permissions",
    response_model=List[RetrievePermissionResponse],
    status_code=200,
)
async def retrieve_permission_by_query_parameters(
    *,
    sqlmodel_session: Session = Depends(get_sqlmodel_session),
    offset: int = 0,
    limit: int = Query(default=100, lte=100),
    name: str = Query(default=None),
) -> list[Permission] | None:
    """Search permission by name."""

    query_parameters = PermissionQueryParameters(offset=offset, limit=limit, name=name)

    retrieved_permission = await retrieve_by_query_parameters(
        sqlmodel_session=sqlmodel_session, query_parameters=query_parameters
    )

    return retrieved_permission


@router.post(
    path="/api/v1/permissions", response_model=CreatePermissionResponse, status_code=201
)
async def create_permission(
    *,
    sqlmodel_session: Session = Depends(get_sqlmodel_session),
    permission: CreatePermissionRequest,
) -> Permission | None:
    """Creates permission."""

    retrieved_permission = await retrieve_by_name(
        sqlmodel_session=sqlmodel_session, permission_name=permission.name
    )

    if retrieved_permission:
        raise PermissionAlreadyExistsException

    created_permission = await create(
        sqlmodel_session=sqlmodel_session, permission=permission
    )

    return created_permission


@router.put(
    path="/api/v1/permission/{permission_id}",
    response_model=UpdatePermissionResponse,
    status_code=200,
)
async def update_permission(
    *,
    sqlmodel_session: Session = Depends(get_sqlmodel_session),
    redis_client: Redis = Depends(get_redis_client),
    permission_id: int,
    permission: UpdatePermissionRequest,
) -> Permission | None:
    """Updates permission."""

    retrieved_permission = await retrieve_by_id(
        sqlmodel_session=sqlmodel_session,
        redis_client=redis_client,
        permission_id=permission_id,
    )

    if not retrieved_permission:
        raise PermissionNotFoundException

    updated_permission = await update(
        sqlmodel_session=sqlmodel_session,
        retrieved_permission=retrieved_permission,
        permission=permission,
    )

    return updated_permission


@router.delete(
    path="/api/v1/permission/{permission_id}",
    response_model=DeletePermissionResponse,
    status_code=200,
)
async def delete_permission(
    *,
    sqlmodel_session: Session = Depends(get_sqlmodel_session),
    redis_client=Depends(get_redis_client),
    permission_id: int,
) -> Permission | None:
    """Deletes permission."""

    retrieved_permission = await retrieve_by_id(
        sqlmodel_session=sqlmodel_session,
        redis_client=redis_client,
        permission_id=permission_id,
    )

    if not retrieved_permission:
        raise PermissionNotFoundException

    deleted_permission = await delete(
        sqlmodel_session=sqlmodel_session, retrieved_permission=retrieved_permission
    )

    return deleted_permission
