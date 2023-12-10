from typing import List
from sqlmodel import Session
from fastapi import Query, Depends, APIRouter
from .exceptions import ExecutionNotFoundException, ExecutionAlreadyExistsException
from .schemas import (
    RetrieveExecutionResponse,
    CreateExecutionRequest,
    CreateExecutionResponse,
    ExecutionQueryParameters,
    UpdateExecutionRequest,
    UpdateExecutionResponse,
    DeleteExecutionResponse,
)
from .service import (
    create,
    retrieve_by_id,
    retrieve_by_name,
    retrieve_by_query_parameters,
    update,
    delete,
)
from ..database.database import get_session

router = APIRouter(tags=["execution"])


@router.get(
    path="/api/v1/execution/{id}",
    response_model=RetrieveExecutionResponse,
    status_code=200,
)
def retrieve_execution_by_id(*, session: Session = Depends(get_session), id: int):
    """Retrieve execution by id."""

    retrieved_execution = retrieve_by_id(session=session, id=id)

    if not retrieved_execution:
        raise ExecutionNotFoundException

    return retrieved_execution


@router.get(
    path="/api/v1/executions",
    response_model=List[RetrieveExecutionResponse],
    status_code=200,
)
def retrieve_execution_by_query_parameters(
    *,
    session: Session = Depends(get_session),
    offset: int = 0,
    limit: int = Query(default=100, lte=100),
    name: str = None,
):
    """Search execution by name."""

    query_execution = ExecutionQueryParameters(offset=offset, limit=limit, name=name)

    retrieved_execution = retrieve_by_query_parameters(
        session=session, query_parameters=query_execution
    )

    return retrieved_execution


@router.post(
    path="/api/v1/executions", response_model=CreateExecutionResponse, status_code=201
)
def create_execution(
    *, session: Session = Depends(get_session), execution: CreateExecutionRequest
):
    """Creates execution."""

    retrieved_execution = retrieve_by_name(session=session, name=execution.name)

    if retrieved_execution:
        raise ExecutionAlreadyExistsException

    created_execution = create(session=session, execution=execution)

    return created_execution


@router.put(
    path="/api/v1/execution/{id}",
    response_model=UpdateExecutionResponse,
    status_code=200,
)
def update_execution(
    *,
    session: Session = Depends(get_session),
    id: int,
    execution: UpdateExecutionRequest,
):
    """Updates repository."""

    retrieved_execution = retrieve_by_id(session=session, id=id)

    if not retrieved_execution:
        raise ExecutionNotFoundException

    updated_execution = update(
        session=session, retrieved_execution=retrieved_execution, execution=execution
    )

    return updated_execution


@router.delete(
    path="/api/v1/execution/{id}",
    response_model=DeleteExecutionResponse,
    status_code=200,
)
def delete_repository(*, session: Session = Depends(get_session), id: int):
    """Deletes execution."""

    retrieved_execution = retrieve_by_id(session=session, id=id)

    if not retrieved_execution:
        raise ExecutionNotFoundException

    deleted_execution = delete(session=session, retrieved_execution=retrieved_execution)

    return deleted_execution
