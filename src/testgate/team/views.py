import smtplib

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from .service import *
from .schemas import *
from ..user.views import allow_create_resource

from ..database.database import get_session

team_router = APIRouter(tags=["teams"])

TeamNotFoundException = HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                      detail="A team with this id does not exist")

TeamAlreadyExistsException = HTTPException(status_code=status.HTTP_409_CONFLICT,
                                           detail="A team with this id already exists")


@team_router.get(path="/api/v1/team/{id}",
                 response_model=None,
                 status_code=200,
                 dependencies=[Depends(allow_create_resource)])
def retrieve_team_by_id(*, session: Session = Depends(get_session), id: int):
    """Retrieves team by id."""

    retrieved_team = retrieve_by_id(session=session, id=id)

    if not retrieved_team:
        raise TeamNotFoundException

    return retrieved_team


@team_router.get(path="/api/v1/teams",
                 response_model=List[RetrieveTeamResponseModel],
                 status_code=200,
                 dependencies=[Depends(allow_create_resource)])
def retrieve_team_by_query_parameters(*, session: Session = Depends(get_session), name: str = None):
    """Search role by name"""
    query_parameters = {"name": name}
    searched_role = retrieve_by_query_parameters(session=session, query_parameters=query_parameters)
    return searched_role


@team_router.post(path="/api/v1/team",
                  response_model=CreateTeamResponseModel,
                  status_code=201,
                  dependencies=[Depends(allow_create_resource)])
def create_team(*, session: Session = Depends(get_session), team: CreateTeamRequestModel):
    """Create team"""

    retrieved_team = retrieve_by_name(session=session, name=team.name)

    if retrieved_team:
        raise TeamAlreadyExistsException

    created_team = create(session=session, team=team)

    return created_team


@team_router.put(path="/api/v1/team/{id}",
                 response_model=UpdateTeamResponseModel,
                 status_code=200,
                 dependencies=[Depends(allow_create_resource)])
def update_team(*, session: Session = Depends(get_session), id: int, team: UpdateTeamRequestModel):
    """Update team"""
    retrieved_team = retrieve_by_id(session=session, id=id)

    if not retrieved_team:
        raise TeamNotFoundException

    updated_team = update(session=session, retrieved_team=retrieved_team, team=team)

    return updated_team


@team_router.delete(path="/api/v1/team/{id}",
                    response_model=DeleteTeamResponseModel,
                    status_code=200,
                    dependencies=[Depends(allow_create_resource)])
def delete_role(*, session: Session = Depends(get_session), id: int):
    """Delete team"""

    retrieved_team = retrieve_by_id(session=session, id=id)

    if not retrieved_team:
        raise TeamNotFoundException

    deleted_team = delete(session=session, retrieved_team=retrieved_team)

    return deleted_team
