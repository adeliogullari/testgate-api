import smtplib

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from .service import *
from .schemas import *
from ..auth.views import allow_create_resource

from ..database.database import get_session

team_router = APIRouter(tags=["workspaces"])

WorkspaceNotFoundException = HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                      detail="A project with this id does not exist")

WorkspaceAlreadyExistsException = HTTPException(status_code=status.HTTP_409_CONFLICT,
                                           detail="A project with this id already exists")


@team_router.get(path="/api/v1/workspace/{id}",
                 response_model=RetrieveWorkspaceResponseModel,
                 status_code=200,
                 dependencies=[Depends(allow_create_resource)])
def retrieve_workspace_by_id(*, session: Session = Depends(get_session), id: int):
    """Retrieves project by id."""

    retrieved_workspace = retrieve_workspace_by_id(session=session, id=id)

    if not retrieved_workspace:
        raise WorkspaceNotFoundException

    return retrieved_workspace


# @team_router.get(path="/api/v1/workspaces",
#                  response_model=List[RetrieveWorkspaceResponseModel],
#                  status_code=200,
#                  dependencies=[Depends(allow_create_resource)])
# def search_team(*, session: Session = Depends(get_session), name: str = None):
#     """Search role by name"""
#     query_parameters = {"name": name}
#     searched_workspace = search_workspace_service(session=session, query_parameters=query_parameters)
#     return searched_workspace


@team_router.post(path="/api/v1/workspace",
                  response_model=CreateWorkspaceResponseModel,
                  status_code=201,
                  dependencies=[Depends(allow_create_resource)])
def create_workspace(*, session: Session = Depends(get_session), workspace: CreateWorkspaceRequestModel):
    """Create project"""

    retrieved_workspace = retrieve_workspace_by_name_service(session=session, name=workspace.name)

    if retrieved_workspace:
        raise WorkspaceAlreadyExistsException

    created_workspace = create_workspace_service(session=session, workspace=workspace)

    return created_workspace


# @team_router.put(path="/api/v1/team/{id}",
#                  response_model=UpdateWorkspaceResponseModel,
#                  status_code=200,
#                  dependencies=[Depends(allow_create_resource)])
# def update_team(*, session: Session = Depends(get_session), id: int, project: UpdateWorkspaceRequestModel):
#     """Update project"""
#     retrieved_team = retrieve_workspace_by_id(session=session, id=id)
#
#     if not retrieved_team:
#         raise WorkspaceNotFoundException
#
#     updated_team = update_workspace_service(session=session, retrieved_team=retrieved_team, team=team)
#
#     return updated_team


@team_router.delete(path="/api/v1/team/{id}",
                    response_model=DeleteWorkspaceResponseModel,
                    status_code=200,
                    dependencies=[Depends(allow_create_resource)])
def delete_workspace(*, session: Session = Depends(get_session), id: int):
    """Delete project"""

    retrieved_workspace = retrieve_workspace_by_id(session=session, id=id)

    if not retrieved_workspace:
        raise WorkspaceNotFoundException

    deleted_workspace = delete_workspace_by_id_service(session=session, retrieved_workspace=retrieved_workspace)

    return deleted_workspace
