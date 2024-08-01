import json
from typing import Any, Sequence
from sqlmodel import select, Session
from redis.asyncio.client import Redis
from src.testgate.execution.models import Execution
from src.testgate.execution.schemas import (
    CreateExecutionRequest,
    ExecutionQueryParameters,
    UpdateExecutionRequest,
)


async def create(
    *, sqlmodel_session: Session, redis_client: Redis, execution: CreateExecutionRequest
) -> Execution:
    """Creates a new execution object."""

    created_execution = Execution(name=execution.name, result=execution.result)

    sqlmodel_session.add(created_execution)
    sqlmodel_session.commit()
    sqlmodel_session.refresh(created_execution)

    await redis_client.set(
        name=f"execution_{created_execution.id}",
        value=created_execution.model_dump_json(),
    )

    return created_execution


async def retrieve_by_id(
    *, sqlmodel_session: Session, redis_client: Redis, execution_id: int
) -> Execution:
    """Returns an execution object based on the given id."""

    if cached_execution := await redis_client.get(name=f"execution_{execution_id}"):
        return Execution(**json.loads(cached_execution))

    if retrieved_execution := sqlmodel_session.exec(
        select(Execution).where(Execution.id == execution_id)
    ).one_or_none():
        await redis_client.set(
            name=f"execution_{execution_id}",
            value=retrieved_execution.model_dump_json(),
        )

    return retrieved_execution


async def retrieve_by_query_parameters(
    *, sqlmodel_session: Session, query_parameters: ExecutionQueryParameters
) -> Sequence[Execution]:
    """Return list of execution objects based on the given query parameters."""

    offset = query_parameters.offset
    limit = query_parameters.limit

    statement: Any = select(Execution).offset(offset).limit(limit)

    for attr, value in query_parameters.model_dump(
        exclude={"offset", "limit"}, exclude_none=True
    ).items():
        statement = statement.filter(getattr(Execution, attr) == value)

    retrieved_executions = sqlmodel_session.exec(statement).all()

    return retrieved_executions


async def update(
    *,
    sqlmodel_session: Session,
    redis_client: Redis,
    retrieved_execution: Execution,
    execution: UpdateExecutionRequest,
) -> Execution:
    """Updates an existing execution object."""

    retrieved_execution.name = execution.name
    updated_execution = retrieved_execution

    sqlmodel_session.add(updated_execution)
    sqlmodel_session.commit()
    sqlmodel_session.refresh(updated_execution)

    await redis_client.set(
        name=f"execution_{updated_execution.id}",
        value=updated_execution.model_dump_json(),
    )

    return updated_execution


async def delete(
    *, sqlmodel_session: Session, redis_client: Redis, retrieved_execution: Execution
) -> Execution:
    """Deletes an existing execution object."""

    sqlmodel_session.delete(retrieved_execution)
    sqlmodel_session.commit()

    await redis_client.delete(f"execution_{retrieved_execution.id}")

    return retrieved_execution
