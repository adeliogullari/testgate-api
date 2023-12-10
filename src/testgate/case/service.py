from typing import Optional
from sqlmodel import select, Session
from .models import Case, CaseResult
from .schemas import CreateCaseRequestModel, UpdateCaseRequestModel


def create(*, session: Session, case: CreateCaseRequestModel) -> Optional[Case]:
    """Creates a new case object."""

    created_case = Case()
    result = CaseResult()
    created_case.name = case.name
    created_case.description = case.description
    created_case.result = result

    session.add(created_case)
    session.commit()
    session.refresh(created_case)

    return created_case


def retrieve_by_id(*, session: Session, id: int) -> Optional[Case]:
    """Returns a case object based on the given id."""

    statement = select(Case).where(Case.id == id)

    retrieved_case = session.exec(statement).one_or_none()

    return retrieved_case


def update(
    *, session: Session, retrieved_case: Case, case: UpdateCaseRequestModel
) -> Optional[Case]:
    """Updates an existing case object."""

    retrieved_case.name = case.name
    updated_case = retrieved_case

    session.add(updated_case)
    session.commit()
    session.refresh(updated_case)

    return updated_case


def delete(*, session: Session, retrieved_case: Case) -> Optional[Case]:
    """Deletes an existing case object."""

    session.delete(retrieved_case)
    session.commit()

    return retrieved_case
