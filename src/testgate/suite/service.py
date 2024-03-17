from typing import Any
from sqlmodel import select, Session
from .models import Suite, SuiteResult
from .schemas import CreateSuiteRequestModel, UpdateSuiteRequestModel


async def create(
    *, sqlmodel_session: Session, suite: CreateSuiteRequestModel
) -> Suite | None:
    """Creates a new suite object."""

    created_suite = Suite()
    suite_result = SuiteResult()
    created_suite.name = suite.name
    created_suite.result = suite_result

    sqlmodel_session.add(created_suite)
    sqlmodel_session.commit()
    sqlmodel_session.refresh(created_suite)

    return created_suite


async def retrieve_by_id(*, sqlmodel_session: Session, id: int) -> Suite | None:
    """Returns a suite object based on the given id."""

    statement: Any = select(Suite).where(Suite.id == id)

    retrieved_suite = sqlmodel_session.exec(statement).one_or_none()

    return retrieved_suite


async def retrieve_by_name(*, sqlmodel_session: Session, name: str) -> Suite | None:
    """Return a suite object based on the given name."""

    statement: Any = select(Suite).where(Suite.name == name)

    retrieved_suite = sqlmodel_session.exec(statement).one_or_none()

    return retrieved_suite


async def update(
    *, sqlmodel_session: Session, retrieved_suite: Suite, suite: UpdateSuiteRequestModel
) -> Suite | None:
    """Updates an existing suite object."""

    retrieved_suite.name = suite.name
    updated_suite = retrieved_suite

    sqlmodel_session.add(updated_suite)
    sqlmodel_session.commit()
    sqlmodel_session.refresh(updated_suite)

    return updated_suite


async def delete(*, sqlmodel_session: Session, retrieved_suite: Suite) -> Suite | None:
    """Deletes an existing suite object."""

    sqlmodel_session.delete(retrieved_suite)
    sqlmodel_session.commit()

    return retrieved_suite
