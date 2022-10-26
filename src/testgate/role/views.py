import smtplib

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from .service import *
from .schemas import *
from ..auth.views import allow_create_resource

from ..database.database import get_session

role_router = APIRouter(tags=["roles"])

RoleNotFoundException = HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                      detail="A role with this id does not exist")

RoleAlreadyExistsException = HTTPException(status_code=status.HTTP_409_CONFLICT,
                                           detail="A role with this id already exists")


@role_router.get(path="/api/v1/role/{id}",
                 response_model=None,
                 status_code=200,
                 dependencies=[Depends(allow_create_resource)])
def retrieve_role_by_id(*, session: Session = Depends(get_session), id: int):
    """Retrieves role by id."""

    retrieved_role = retrieve_role_by_id_service(session=session, id=id)

    if not retrieved_role:
        raise RoleNotFoundException

    return retrieved_role


@role_router.get(path="/api/v1/roles",
                 response_model=List[RetrieveRoleResponseModel],
                 status_code=200,
                 dependencies=[Depends(allow_create_resource)])
def search_role(*, session: Session = Depends(get_session), name: str = None):
    """Search role by name"""
    query_parameters = {"name": name}
    searched_role = search_role_service(session=session, query_parameters=query_parameters)
    return searched_role


@role_router.post(path="/api/v1/role",
                  response_model=CreateRoleResponseModel,
                  status_code=201,
                  dependencies=[Depends(allow_create_resource)])
def create_role(*, session: Session = Depends(get_session), role: CreateRoleRequestModel):
    """Create role"""
    retrieved_role = retrieve_role_by_name_service(session=session, name=role.name)

    if retrieved_role:
        raise RoleAlreadyExistsException

    created_role = create_role_service(session=session, role=role)

    return created_role


@role_router.put(path="/api/v1/role/{id}",
                 response_model=UpdateRoleResponseModel,
                 status_code=200,
                 dependencies=[Depends(allow_create_resource)])
def update_role(*, session: Session = Depends(get_session), id: int, role: UpdateRoleRequestModel):
    """Update role"""
    retrieved_role = retrieve_role_by_id_service(session=session, id=id)

    if not retrieved_role:
        raise RoleNotFoundException

    updated_role = update_role_service(session=session, retrieved_role=retrieved_role, role=role)

    return updated_role


@role_router.delete(path="/api/v1/role/{id}",
                    response_model=DeleteRoleResponseModel,
                    status_code=200,
                    dependencies=[Depends(allow_create_resource)])
def delete_role(*, session: Session = Depends(get_session), id: int):
    """Delete role"""
    retrieved_role = retrieve_role_by_id_service(session=session, id=id)

    if not retrieved_role:
        raise RoleNotFoundException

    deleted_role = delete_role_by_id_service(session=session, retrieved_role=retrieved_role)

    return deleted_role
