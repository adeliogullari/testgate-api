from typing import List
from sqlmodel import Session
from fastapi import Query, Depends, APIRouter
from redis.asyncio.client import Redis
from .exceptions import ExecutionNotFoundException, ExecutionAlreadyExistsException
from .models import Execution
from .schemas import (
    RetrieveExecutionResponse,
    CreateExecutionRequest,
    CreateExecutionResponse,
    ExecutionQueryParameters,
    UpdateExecutionRequest,
    UpdateExecutionResponse,
    DeleteExecutionResponse,
)
import src.testgate.execution.service as execution_service
from src.testgate.database.service import get_sqlmodel_session, get_redis_client

router = APIRouter(tags=["executions"])


@router.get(
    path="/api/v1/executions/{execution_id}",
    response_model=RetrieveExecutionResponse,
    status_code=200,
)
async def retrieve_execution_by_id(
    *,
    sqlmodel_session: Session = Depends(get_sqlmodel_session),
    redis_client: Redis = Depends(get_redis_client),
    execution_id: int,
) -> Execution | None:
    """Retrieve execution by id."""

    retrieved_execution = await execution_service.retrieve_by_id(
        sqlmodel_session=sqlmodel_session,
        redis_client=redis_client,
        execution_id=execution_id,
    )

    if not retrieved_execution:
        raise ExecutionNotFoundException

    return retrieved_execution


@router.get(
    path="/api/v1/executions",
    response_model=List[RetrieveExecutionResponse],
    status_code=200,
)
async def retrieve_execution_by_query_parameters(
    *,
    sqlmodel_session: Session = Depends(get_sqlmodel_session),
    offset: int = 0,
    limit: int = Query(default=100, lte=100),
    name: str = Query(default=None),
) -> list[Execution] | None:
    """Search execution by name."""

    query_execution = ExecutionQueryParameters(offset=offset, limit=limit, name=name)

    retrieved_execution = await execution_service.retrieve_by_query_parameters(
        sqlmodel_session=sqlmodel_session, query_parameters=query_execution
    )

    return retrieved_execution


@router.post(
    path="/api/v1/executions", response_model=CreateExecutionResponse, status_code=201
)
async def create_execution(
    *,
    sqlmodel_session: Session = Depends(get_sqlmodel_session),
    redis_client=Depends(get_redis_client),
    execution: CreateExecutionRequest,
) -> Execution | None:
    """Creates execution."""

    retrieved_execution = await execution_service.retrieve_by_name(
        sqlmodel_session=sqlmodel_session, name=execution.name
    )

    if retrieved_execution:
        raise ExecutionAlreadyExistsException

    created_execution = await execution_service.create(
        sqlmodel_session=sqlmodel_session,
        redis_client=redis_client,
        execution=execution,
    )

    return created_execution


@router.put(
    path="/api/v1/executions/{execution_id}",
    response_model=UpdateExecutionResponse,
    status_code=200,
)
async def update_execution(
    *,
    sqlmodel_session: Session = Depends(get_sqlmodel_session),
    redis_client: Redis = Depends(get_redis_client),
    execution_id: int,
    execution: UpdateExecutionRequest,
) -> Execution | None:
    """Updates repository."""

    retrieved_execution = await execution_service.retrieve_by_id(
        sqlmodel_session=sqlmodel_session,
        redis_client=redis_client,
        execution_id=execution_id,
    )

    if not retrieved_execution:
        raise ExecutionNotFoundException

    updated_execution = await execution_service.update(
        sqlmodel_session=sqlmodel_session,
        redis_client=redis_client,
        retrieved_execution=retrieved_execution,
        execution=execution,
    )

    return updated_execution


@router.delete(
    path="/api/v1/executions/{execution_id}",
    response_model=DeleteExecutionResponse,
    status_code=200,
)
async def delete_repository(
    *,
    sqlmodel_session: Session = Depends(get_sqlmodel_session),
    redis_client: Redis = Depends(get_redis_client),
    execution_id: int,
) -> Execution | None:
    """Deletes execution."""

    retrieved_execution = await execution_service.retrieve_by_id(
        sqlmodel_session=sqlmodel_session,
        redis_client=redis_client,
        execution_id=execution_id,
    )

    if not retrieved_execution:
        raise ExecutionNotFoundException

    deleted_execution = await execution_service.delete(
        sqlmodel_session=sqlmodel_session,
        redis_client=redis_client,
        retrieved_execution=retrieved_execution,
    )

    return deleted_execution
