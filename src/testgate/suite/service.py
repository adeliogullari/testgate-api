from typing import Any, Optional, List
from sqlmodel import select, Session
from .models import Suite
from .schemas import CreateSuiteRequestModel, UpdateSuiteRequestModel


def create(*, session: Session, suite: CreateSuiteRequestModel) -> Optional[Suite]:
    """Creates a new suite object."""

    created_suite = Suite()
    created_suite.name = suite.name
    created_suite.result = suite.result

    session.add(created_suite)
    session.commit()
    session.refresh(created_suite)

    return created_suite


def retrieve_by_id(*, session: Session, id: int) -> Optional[Any]:
    """Returns a suite object based on the given id."""

    statement = select(Suite).where(Suite.id == id)

    retrieved_suite = session.exec(statement).one_or_none()

    return retrieved_suite


def retrieve_by_name(*, session: Session, name: str) -> Optional[Suite]:
    """Return a suite object based on the given name."""

    statement = select(Suite).where(Suite.name == name)

    retrieved_suite = session.exec(statement).one_or_none()

    return retrieved_suite


def update(*, session: Session, retrieved_suite: Suite, suite: UpdateSuiteRequestModel) -> Optional[Suite]:
    """Updates an existing suite object."""

    retrieved_suite.name = suite.name
    updated_suite = retrieved_suite

    session.add(updated_suite)
    session.commit()
    session.refresh(updated_suite)

    return updated_suite


def delete(*, session: Session, retrieved_suite: Suite) -> Optional[Suite]:
    """Deletes an existing suite object."""

    session.delete(retrieved_suite)
    session.commit()

    return retrieved_suite
