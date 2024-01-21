from typing import Optional, List, Any
from sqlmodel import select, Session
from .models import Case, CaseResult
from .schemas import CreateCaseRequestModel, CaseQueryParameters, UpdateCaseRequestModel


def create(*, session: Session, case: CreateCaseRequestModel) -> Case | None:
    """Creates a new case object."""

    created_case = Case()
    created_case.name = case.name
    created_case.description = case.description
    created_case.result = case.result

    session.add(created_case)
    session.commit()
    session.refresh(created_case)

    return created_case


def retrieve_by_id(*, session: Session, case_id: int) -> Case | None:
    """Returns a case object based on the given id."""

    statement: Any = select(Case).where(Case.id == case_id)

    retrieved_case = session.exec(statement).one_or_none()

    return retrieved_case


def retrieve_by_query_parameters(
    *, session: Session, query_parameters: CaseQueryParameters
) -> List[Case] | None:
    """Return list of case objects based on the given query parameters."""

    offset = query_parameters.offset
    limit = query_parameters.limit

    statement: Any = select(Case).offset(offset).limit(limit)

    for attr, value in query_parameters.model_dump(
        exclude={"offset", "limit"}, exclude_none=True
    ).items():
        statement = statement.where(getattr(Case, attr) == value)

    retrieved_case = session.exec(statement).all()

    return retrieved_case


def update(
    *, session: Session, retrieved_case: Case, case: UpdateCaseRequestModel
) -> Case | None:
    """Updates an existing case object."""

    retrieved_case.name = case.name
    retrieved_case.description = case.description
    retrieved_case.result = case.result
    updated_case = retrieved_case

    session.add(updated_case)
    session.commit()
    session.refresh(updated_case)

    return updated_case


def delete(*, session: Session, retrieved_case: Case) -> Case | None:
    """Deletes an existing case object."""

    session.delete(retrieved_case)
    session.commit()

    return retrieved_case
