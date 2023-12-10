from typing import Optional, List
from sqlmodel import select, Session
from src.testgate.execution.models import Execution, ExecutionResult
from src.testgate.execution.schemas import (
    CreateExecutionRequest,
    ExecutionQueryParameters,
    UpdateExecutionRequest,
)


def create(
    *, session: Session, execution: CreateExecutionRequest
) -> Optional[Execution]:
    """Creates a new execution object."""

    created_execution = Execution()
    created_execution.name = execution.name
    created_execution.result = ExecutionResult()

    session.add(created_execution)
    session.commit()
    session.refresh(created_execution)

    return created_execution


def retrieve_by_id(*, session: Session, id: int) -> Optional[Execution]:
    """Return a execution object based on the given id."""

    statement = select(Execution).where(Execution.id == id)

    retrieved_execution = session.exec(statement).one_or_none()

    return retrieved_execution


def retrieve_by_name(*, session: Session, name: str) -> Optional[Execution]:
    """Return a execution object based on the given name."""

    statement = select(Execution).where(Execution.name == name)

    retrieved_execution = session.exec(statement).one_or_none()

    return retrieved_execution


def retrieve_by_query_parameters(
    *, session: Session, query_parameters: ExecutionQueryParameters
) -> Optional[List[Execution]]:
    """Return list of execution objects based on the given query parameters."""

    statement = select(Execution)

    for attr, value in query_parameters.dict().items():
        if value:
            statement = statement.filter(getattr(Execution, attr).like(value))

    retrieved_executions = session.exec(statement).all()

    return retrieved_executions


def update(
    *,
    session: Session,
    retrieved_execution: Execution,
    execution: UpdateExecutionRequest,
) -> Optional[Execution]:
    """Updates an existing execution object."""

    retrieved_execution.name = execution.name
    updated_execution = retrieved_execution

    session.add(updated_execution)
    session.commit()
    session.refresh(updated_execution)

    return updated_execution


def delete(*, session: Session, retrieved_execution: Execution) -> Optional[Execution]:
    """Deletes an existing execution object."""

    session.delete(retrieved_execution)
    session.commit()

    return retrieved_execution
