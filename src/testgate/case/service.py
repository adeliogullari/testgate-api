import json
from typing import Any, Sequence
from sqlmodel import select, Session
from redis.asyncio.client import Redis
from .models import Case
from .schemas import CreateCaseRequestModel, CaseQueryParameters, UpdateCaseRequestModel


async def create(
    *, sqlmodel_session: Session, redis_client: Redis, case: CreateCaseRequestModel
) -> Case:
    """Creates a new case object."""

    created_case = Case(
        name=case.name, description=case.description, result=case.result
    )

    sqlmodel_session.add(created_case)
    sqlmodel_session.commit()
    sqlmodel_session.refresh(created_case)

    await redis_client.set(
        name=f"case_{created_case.id}", value=created_case.model_dump_json()
    )

    return created_case


async def retrieve_by_id(
    *, sqlmodel_session: Session, redis_client: Redis, case_id: int
) -> Case | None:
    """Returns a case object based on the given id."""

    if cached_case := await redis_client.get(name=f"case_{case_id}"):
        return Case(**json.loads(cached_case))

    if retrieved_case := sqlmodel_session.exec(
        select(Case).where(Case.id == case_id)
    ).one_or_none():
        await redis_client.set(
            name=f"case_{case_id}", value=retrieved_case.model_dump_json()
        )

    return retrieved_case


async def retrieve_by_query_parameters(
    *, sqlmodel_session: Session, query_parameters: CaseQueryParameters
) -> Sequence[Case]:
    """Returns list of case objects based on the given query parameters."""

    offset = query_parameters.offset
    limit = query_parameters.limit

    statement: Any = select(Case).offset(offset).limit(limit)

    for attr, value in query_parameters.model_dump(
        exclude={"offset", "limit"}, exclude_none=True
    ).items():
        statement = statement.where(getattr(Case, attr) == value)

    retrieved_cases = sqlmodel_session.exec(statement).all()

    return retrieved_cases


async def update(
    *,
    sqlmodel_session: Session,
    redis_client: Redis,
    retrieved_case: Case,
    case: UpdateCaseRequestModel,
) -> Case:
    """Updates an existing case object."""

    retrieved_case.name = case.name
    retrieved_case.description = case.description
    retrieved_case.result = case.result
    updated_case = retrieved_case

    sqlmodel_session.add(updated_case)
    sqlmodel_session.commit()
    sqlmodel_session.refresh(updated_case)

    await redis_client.set(
        name=f"case_{updated_case.id}", value=updated_case.model_dump_json()
    )

    return updated_case


async def delete(
    *, sqlmodel_session: Session, redis_client: Redis, retrieved_case: Case
) -> Case:
    """Deletes an existing case object."""

    sqlmodel_session.delete(retrieved_case)
    sqlmodel_session.commit()

    await redis_client.delete(f"case_{retrieved_case.id}")

    return retrieved_case
