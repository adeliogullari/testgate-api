from typing import List
from sqlmodel import Session
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
from .service import (
    create,
    retrieve_by_id,
    retrieve_by_name,
    retrieve_by_query_parameters,
    update,
    delete,
)
from src.testgate.database.service import get_session

router = APIRouter(tags=["permissions"])


@router.get(
    path="/api/v1/permission/{id}",
    response_model=RetrievePermissionResponse,
    status_code=200,
)
def retrieve_permission_by_id(*, session: Session = Depends(get_session), id: int):
    """Retrieve permission by id."""

    retrieved_permission = retrieve_by_id(session=session, id=id)

    if not retrieved_permission:
        raise PermissionNotFoundException

    return retrieved_permission


@router.get(
    path="/api/v1/permissions",
    response_model=List[RetrievePermissionResponse],
    status_code=200,
)
def retrieve_permission_by_query_parameters(
    *,
    session: Session = Depends(get_session),
    offset: int = 0,
    limit: int = Query(default=100, lte=100),
    name: str = None,
):
    """Search permission by name."""

    query_parameters = PermissionQueryParameters(offset=offset, limit=limit, name=name)

    retrieved_permission = retrieve_by_query_parameters(
        session=session, query_parameters=query_parameters
    )

    return retrieved_permission


@router.post(
    path="/api/v1/permissions", response_model=CreatePermissionResponse, status_code=201
)
def create_permission(
    *, session: Session = Depends(get_session), permission: CreatePermissionRequest
):
    """Creates permission."""

    retrieved_permission = retrieve_by_name(session=session, name=permission.name)

    if retrieved_permission:
        raise PermissionAlreadyExistsException

    created_permission = create(session=session, permission=permission)

    return created_permission


@router.put(
    path="/api/v1/permission/{id}",
    response_model=UpdatePermissionResponse,
    status_code=200,
)
def update_permission(
    *,
    session: Session = Depends(get_session),
    id: int,
    permission: UpdatePermissionRequest,
):
    """Updates permission."""

    retrieved_permission = retrieve_by_id(session=session, id=id)

    if not retrieved_permission:
        raise PermissionNotFoundException

    updated_permission = update(
        session=session,
        retrieved_permission=retrieved_permission,
        permission=permission,
    )

    return updated_permission


@router.delete(
    path="/api/v1/permission/{id}",
    response_model=DeletePermissionResponse,
    status_code=200,
)
def delete_permission(*, session: Session = Depends(get_session), id: int):
    """Deletes permission."""

    retrieved_permission = retrieve_by_id(session=session, id=id)

    if not retrieved_permission:
        raise PermissionNotFoundException

    deleted_permission = delete(
        session=session, retrieved_permission=retrieved_permission
    )

    return deleted_permission
