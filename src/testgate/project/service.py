from typing import Optional, List
from sqlmodel import select, Session
from .models import Project
from .schemas import CreateProjectRequestModel, UpdateProjectRequestModel


def retrieve_by_id(*, session: Session, id: int) -> Optional[Project]:
    """Returns a project object based on the given role id."""

    statement = select(Project).where(Project.id == id)

    retrieved_project = session.exec(statement).one_or_none()

    return retrieved_project


def retrieve_by_name(*, session: Session, name: str) -> Optional[Project]:
    """Returns a team object based on the given team name."""

    statement = select(Project).where(Project.name == name)

    retrieved_team = session.exec(statement).one_or_none()

    return retrieved_team


def retrieve_by_query_parameters(*, session: Session, query_parameters: dict) -> Optional[List[Project]]:
    """Returns a team object based on the given query parameters."""

    statement = select(Project)

    for attr, value in query_parameters.items():
        if value:
            statement = statement.filter(getattr(Project, attr).like(value))

    searched_role = session.exec(statement).all()

    return searched_role


def create(*, session: Session, project: CreateProjectRequestModel) -> Optional[Project]:
    """Creates a new team."""

    created_project = Project()
    created_project.name = project.name

    session.add(created_project)
    session.commit()
    session.refresh(created_project)

    return created_project


def update(*, session: Session, retrieved_project: Project, project: UpdateProjectRequestModel) -> Optional[Project]:
    """Updates an existing project."""

    # for attr, value in team.dict().items():
    #     if value:
    #         setattr(retrieved_team, attr, value)

    retrieved_project.name = project.name
    updated_project= retrieved_project

    session.add(updated_project)
    session.commit()
    session.refresh(updated_project)

    return updated_project


def delete(*, session: Session, retrieved_project: Project) -> Optional[Project]:
    """Deletes an existing team."""

    session.delete(retrieved_project)
    session.commit()

    return retrieved_project
