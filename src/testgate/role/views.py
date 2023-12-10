from typing import List
from sqlmodel import Session
from fastapi import status, Depends, APIRouter, HTTPException
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
    CreateRoleRequestModel,
    CreateRoleResponseModel,
    UpdateRoleRequestModel,
    UpdateRoleResponseModel,
    DeleteRoleResponseModel,
)
from ..user.views import allow_create_resource
from ..database.database import get_session

router = APIRouter(tags=["roles"])

RoleNotFoundException = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND, detail="A role with that id does not exist"
)

RoleAlreadyExistsException = HTTPException(
    status_code=status.HTTP_409_CONFLICT, detail="A role with that id already exists"
)


@router.get(
    path="/api/v1/role/{id}",
    response_model=None,
    status_code=200,
    dependencies=[Depends(allow_create_resource)],
)
def retrieve_role_by_id(*, session: Session = Depends(get_session), id: int):
    """Retrieve role by id."""

    retrieved_role = retrieve_by_id(session=session, id=id)

    if not retrieved_role:
        raise RoleNotFoundException

    return retrieved_role


@router.get(
    path="/api/v1/roles",
    response_model=List[RetrieveRoleResponseModel],
    status_code=200,
    dependencies=[Depends(allow_create_resource)],
)
def retrieve_role_by_query_parameters(
    *, session: Session = Depends(get_session), name: str = None
):
    """Search role by name."""

    retrieved_role = retrieve_by_query_parameters(
        session=session, query_parameters={"name": name}
    )

    return retrieved_role


@router.post(
    path="/api/v1/role",
    response_model=CreateRoleResponseModel,
    status_code=201,
    dependencies=[Depends(allow_create_resource)],
)
def create_role(
    *, session: Session = Depends(get_session), role: CreateRoleRequestModel
):
    """Creates role."""

    retrieved_role = retrieve_by_name(session=session, name=role.name)

    if retrieved_role:
        raise RoleAlreadyExistsException

    created_role = create(session=session, role=role)

    return created_role


@router.put(
    path="/api/v1/role/{id}",
    response_model=UpdateRoleResponseModel,
    status_code=200,
    dependencies=[Depends(allow_create_resource)],
)
def update_role(
    *, session: Session = Depends(get_session), id: int, role: UpdateRoleRequestModel
):
    """Updates role."""

    retrieved_role = retrieve_by_id(session=session, id=id)

    if not retrieved_role:
        raise RoleNotFoundException

    updated_role = update(session=session, retrieved_role=retrieved_role, role=role)

    return updated_role


@router.delete(
    path="/api/v1/role/{id}",
    response_model=DeleteRoleResponseModel,
    status_code=200,
    dependencies=[Depends(allow_create_resource)],
)
def delete_role(*, session: Session = Depends(get_session), id: int):
    """Deletes role."""

    retrieved_role = retrieve_by_id(session=session, id=id)

    if not retrieved_role:
        raise RoleNotFoundException

    deleted_role = delete(session=session, retrieved_role=retrieved_role)

    return deleted_role
