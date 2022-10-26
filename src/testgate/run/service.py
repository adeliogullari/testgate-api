from typing import Any, Optional, List
from sqlmodel import select, Session
from .models import Run
from .schemas import CreateRunRequestModel, UpdateRunRequestModel


def create(*, session: Session, run: CreateRunRequestModel) -> Optional[Run]:
    """Creates a new run object."""

    created_run = Run()
    created_run.name = run.name
    created_run.result = run.result

    session.add(created_run)
    session.commit()
    session.refresh(created_run)

    return created_run


def retrieve_by_id(*, session: Session, id: int) -> Optional[Any]:
    """Return a run object based on the given id."""

    statement = select(Run).where(Run.id == id)

    retrieved_run = session.exec(statement).one_or_none()

    return retrieved_run


def retrieve_by_name(*, session: Session, name: str) -> Optional[Run]:
    """Return a run object based on the given name."""

    statement = select(Run).where(Run.name == name)

    retrieved_run = session.exec(statement).one_or_none()

    return retrieved_run


def retrieve_by_query_parameters(*, session: Session, query_parameters: dict) -> Optional[List[Run]]:
    """Return list of run objects based on the given query parameters."""

    statement = select(Run)

    for attr, value in query_parameters.items():
        if value:
            statement = statement.filter(getattr(Run, attr).like(value))

    retrieved_runs = session.exec(statement).all()

    return retrieved_runs


def update(*, session: Session, retrieved_run: Run, run: UpdateRunRequestModel) -> Optional[Run]:
    """Updates an existing run object."""

    retrieved_run.name = run.name
    updated_run = retrieved_run

    session.add(updated_run)
    session.commit()
    session.refresh(updated_run)

    return updated_run


def delete(*, session: Session, retrieved_run: Run) -> Optional[Run]:
    """Deletes an existing run object."""

    session.delete(retrieved_run)
    session.commit()

    return retrieved_run
