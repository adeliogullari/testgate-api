from typing import List

from sqlmodel import Session
from redis.asyncio import Redis
from fastapi import Depends, APIRouter, Query
from .service import (
    create,
    retrieve_by_id,
    retrieve_by_query_parameters,
    update,
    delete,
)
from .exceptions import CaseNotFoundException
from .schemas import (
    RetrieveCaseResponseModel,
    CaseQueryParameters,
    CreateCaseRequestModel,
    CreateCaseResponseModel,
    UpdateCaseRequestModel,
    UpdateCaseResponseModel,
    DeleteCaseResponseModel,
)
from .models import Case
from src.testgate.database.service import get_sqlmodel_session, get_redis_client

router = APIRouter(tags=["cases"])


@router.post(
    path="/api/v1/cases",
    response_model=CreateCaseResponseModel,
    status_code=201,
)
async def create_case(
    *,
    sqlmodel_session: Session = Depends(get_sqlmodel_session),
    redis_client: Redis = Depends(get_redis_client),
    case: CreateCaseRequestModel,
) -> Case | None:
    """Creates case."""

    created_case = await create(
        sqlmodel_session=sqlmodel_session, redis_client=redis_client, case=case
    )

    return created_case


@router.get(
    path="/api/v1/cases/{case_id}",
    response_model=RetrieveCaseResponseModel,
    status_code=200,
)
async def retrieve_case_by_id(
    *,
    sqlmodel_session: Session = Depends(get_sqlmodel_session),
    redis_client: Redis = Depends(get_redis_client),
    case_id: int,
) -> Case | None:
    """Retrieves case by id."""
    retrieved_case = await retrieve_by_id(
        sqlmodel_session=sqlmodel_session, redis_client=redis_client, case_id=case_id
    )

    if not retrieved_case:
        raise CaseNotFoundException

    return retrieved_case


@router.get(
    path="/api/v1/cases",
    response_model=List[RetrieveCaseResponseModel],
    status_code=200,
)
async def retrieve_case_by_query_parameters(
    *,
    sqlmodel_session: Session = Depends(get_sqlmodel_session),
    offset: int = Query(default=0),
    limit: int = Query(default=100, lte=100),
    name: str = Query(default=None),
) -> list[Case] | None:
    """Search case by name."""

    query_parameters = CaseQueryParameters(offset=offset, limit=limit, name=name)

    retrieved_cases = await retrieve_by_query_parameters(
        sqlmodel_session=sqlmodel_session, query_parameters=query_parameters
    )

    return retrieved_cases


@router.put(
    path="/api/v1/cases/{case_id}",
    response_model=UpdateCaseResponseModel,
    status_code=200,
)
async def update_case(
    *,
    sqlmodel_session: Session = Depends(get_sqlmodel_session),
    redis_client: Redis = Depends(get_redis_client),
    case_id: int,
    case: UpdateCaseRequestModel,
) -> Case | None:
    """Updates case."""

    retrieved_case = await retrieve_by_id(
        sqlmodel_session=sqlmodel_session, redis_client=redis_client, case_id=case_id
    )

    if not retrieved_case:
        raise CaseNotFoundException

    updated_case = await update(
        sqlmodel_session=sqlmodel_session,
        redis_client=redis_client,
        retrieved_case=retrieved_case,
        case=case,
    )

    return updated_case


@router.delete(
    path="/api/v1/cases/{case_id}",
    response_model=DeleteCaseResponseModel,
    status_code=200,
)
async def delete_case(
    *,
    sqlmodel_session: Session = Depends(get_sqlmodel_session),
    redis_client: Redis = Depends(get_redis_client),
    case_id: int,
) -> Case | None:
    """Deletes case."""

    retrieved_case = await retrieve_by_id(
        sqlmodel_session=sqlmodel_session, redis_client=redis_client, case_id=case_id
    )

    if not retrieved_case:
        raise CaseNotFoundException

    deleted_case = await delete(
        sqlmodel_session=sqlmodel_session,
        redis_client=redis_client,
        retrieved_case=retrieved_case,
    )

    return deleted_case
