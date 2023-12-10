from typing import List
from sqlmodel import Session
from fastapi import Query, Depends, APIRouter
from .exceptions import RepositoryNotFoundException, RepositoryAlreadyExistsException
from .schemas import (
    RetrieveRepositoryResponse,
    CreateRepositoryRequest,
    CreateRepositoryResponse,
    RepositoryQueryParameters,
    UpdateRepositoryRequest,
    UpdateRepositoryResponse,
    DeleteRepositoryResponse,
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

router = APIRouter(tags=["repository"])


@router.get(
    path="/api/v1/repository/{id}",
    response_model=RetrieveRepositoryResponse,
    status_code=200,
)
def retrieve_repository_by_id(*, session: Session = Depends(get_session), id: int):
    """Retrieve repository by id."""

    retrieved_repository = retrieve_by_id(session=session, id=id)

    if not retrieved_repository:
        raise RepositoryNotFoundException

    return retrieved_repository


@router.get(
    path="/api/v1/repositories",
    response_model=List[RetrieveRepositoryResponse],
    status_code=200,
)
def retrieve_repository_by_query_parameters(
    *,
    session: Session = Depends(get_session),
    offset: int = 0,
    limit: int = Query(default=100, lte=100),
    name: str = None,
):
    """Search repository by name."""

    query_repository = RepositoryQueryParameters(offset=offset, limit=limit, name=name)

    retrieved_repository = retrieve_by_query_parameters(
        session=session, query_parameters=query_repository
    )

    return retrieved_repository


@router.post(
    path="/api/v1/repositories",
    response_model=CreateRepositoryResponse,
    status_code=201,
)
def create_repository(
    *, session: Session = Depends(get_session), repository: CreateRepositoryRequest
):
    """Creates repository."""

    retrieved_repository = retrieve_by_name(session=session, name=repository.name)

    if retrieved_repository:
        raise RepositoryAlreadyExistsException

    created_repository = create(session=session, repository=repository)

    return created_repository


@router.put(
    path="/api/v1/repository/{id}",
    response_model=UpdateRepositoryResponse,
    status_code=200,
)
def update_repository(
    *,
    session: Session = Depends(get_session),
    id: int,
    repository: UpdateRepositoryRequest,
):
    """Updates repository."""

    retrieved_repository = retrieve_by_id(session=session, id=id)

    if not retrieved_repository:
        raise RepositoryNotFoundException

    updated_repository = update(
        session=session,
        retrieved_repository=retrieved_repository,
        repository=repository,
    )

    return updated_repository


@router.delete(
    path="/api/v1/repository/{id}",
    response_model=DeleteRepositoryResponse,
    status_code=200,
)
def delete_repository(*, session: Session = Depends(get_session), id: int):
    """Deletes repository."""

    retrieved_repository = retrieve_by_id(session=session, id=id)

    if not retrieved_repository:
        raise RepositoryNotFoundException

    deleted_repository = delete(
        session=session, retrieved_repository=retrieved_repository
    )

    return deleted_repository
