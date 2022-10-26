from typing import Optional, List, Dict
from jose import jwt
from sqlmodel import select, Session

from ..role.models import Role
from ..team.models import Team

from .models import Team
from .schemas import RetrieveTeamResponseModel, CreateTeamRequestModel, DeleteTeamResponseModel, UpdateTeamRequestModel


def retrieve_team_by_id_service(*, session: Session, id: int) -> Optional[Team]:
    """Returns a team object based on the given role id."""

    statement = select(Team).where(Team.id == id)

    retrieved_team = session.exec(statement).one_or_none()

    return retrieved_team


def retrieve_team_by_name_service(*, session: Session, name: str) -> Optional[Team]:
    """Returns a team object based on the given team name."""

    statement = select(Team).where(Team.name == name)

    retrieved_team = session.exec(statement).one_or_none()

    return retrieved_team


# def search_role_service(*, session: Session, query_parameters: dict) -> Optional[List[Role]]:
#     """Returns a role object based on the given query parameters."""
#
#     statement = select(Role)
#
#     for attr, value in query_parameters.items():
#         if value:
#             statement = statement.filter(getattr(Role, attr).like(value))
#
#     searched_role = session.exec(statement).all()
#
#     return searched_role


def create_team_service(*, session: Session, team: CreateTeamRequestModel) -> Optional[Team]:
    """Creates a new team."""

    created_team = Team(**team.dict())

    session.add(created_team)
    session.commit()
    session.refresh(created_team)

    return created_team


def update_role_service(*, session: Session, retrieved_team: Team, team: UpdateTeamRequestModel) -> Optional[Team]:
    """Updates an existing team."""

    for attr, value in team.dict().items():
        if value:
            setattr(retrieved_team, attr, value)

    updated_team = Team(**retrieved_team.dict())

    session.add(updated_team)
    session.commit()
    session.refresh(updated_team)

    return updated_team


def delete_team_by_id_service(*, session: Session, retrieved_team: Team) -> Optional[Team]:
    """Deletes an existing team."""

    session.delete(retrieved_team)
    session.commit()

    return retrieved_team
