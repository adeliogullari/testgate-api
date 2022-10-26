from typing import Optional, List
from sqlmodel import select, Session
from .models import Team
from .schemas import CreateTeamRequestModel, UpdateTeamRequestModel


def retrieve_by_id(*, session: Session, id: int) -> Optional[Team]:
    """Returns a team object based on the given role id."""

    statement = select(Team).where(Team.id == id)

    retrieved_team = session.exec(statement).one_or_none()

    return retrieved_team


def retrieve_by_name(*, session: Session, name: str) -> Optional[Team]:
    """Returns a team object based on the given team name."""

    statement = select(Team).where(Team.name == name)

    retrieved_team = session.exec(statement).one_or_none()

    return retrieved_team


def retrieve_by_query_parameters(*, session: Session, query_parameters: dict) -> Optional[List[Team]]:
    """Returns a team object based on the given query parameters."""

    statement = select(Team)

    for attr, value in query_parameters.items():
        if value:
            statement = statement.filter(getattr(Team, attr).like(value))

    searched_role = session.exec(statement).all()

    return searched_role


def create(*, session: Session, team: CreateTeamRequestModel) -> Optional[Team]:
    """Creates a new team."""

    created_team = Team()
    created_team.name = team.name

    session.add(created_team)
    session.commit()
    session.refresh(created_team)

    return created_team


def update(*, session: Session, retrieved_team: Team, team: UpdateTeamRequestModel) -> Optional[Team]:
    """Updates an existing team."""

    # for attr, value in team.dict().items():
    #     if value:
    #         setattr(retrieved_team, attr, value)

    retrieved_team.name = team.name
    updated_team = retrieved_team

    session.add(updated_team)
    session.commit()
    session.refresh(updated_team)

    return updated_team


def delete(*, session: Session, retrieved_team: Team) -> Optional[Team]:
    """Deletes an existing team."""

    session.delete(retrieved_team)
    session.commit()

    return retrieved_team
