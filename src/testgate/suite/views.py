from sqlmodel import Session
from fastapi import status, Depends, APIRouter, HTTPException
from .service import retrieve_by_id, retrieve_by_name, create, update, delete
from .schemas import (
    RetrieveSuiteResponseModel,
    CreateSuiteRequestModel,
    CreateSuiteResponseModel,
    UpdateSuiteRequestModel,
    UpdateSuiteResponseModel,
    DeleteSuiteResponseModel,
)
from src.testgate.suite.models import Suite
from src.testgate.database.service import get_session

router = APIRouter(tags=["suites"])

SuiteNotFoundException = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND, detail="A run with that id does not exist"
)

SuiteAlreadyExistsException = HTTPException(
    status_code=status.HTTP_409_CONFLICT, detail="A run with that id already exists"
)


@router.get(
    path="/api/v1/suite/{id}",
    response_model=RetrieveSuiteResponseModel,
    status_code=200,
)
def retrieve_suite_by_id(
    *, session: Session = Depends(get_session), id: int
) -> Suite | None:
    """Retrieve suite by id."""

    retrieved_suite = retrieve_by_id(session=session, id=id)

    if not retrieved_suite:
        raise SuiteNotFoundException

    return retrieved_suite


@router.post(
    path="/api/v1/suite",
    response_model=CreateSuiteResponseModel,
    status_code=201,
)
def create_suite(
    *, session: Session = Depends(get_session), suite: CreateSuiteRequestModel
) -> Suite | None:
    """Creates suite."""

    retrieved_suite = retrieve_by_name(session=session, name=suite.name)

    if retrieved_suite:
        raise SuiteAlreadyExistsException

    created_suite = create(session=session, suite=suite)

    return created_suite


@router.put(
    path="/api/v1/suite/{id}",
    response_model=UpdateSuiteResponseModel,
    status_code=200,
)
def update_suite(
    *, session: Session = Depends(get_session), id: int, suite: UpdateSuiteRequestModel
) -> Suite | None:
    """Updates suite."""

    retrieved_suite = retrieve_by_id(session=session, id=id)

    if not retrieved_suite:
        raise SuiteNotFoundException

    updated_suite = update(
        session=session, retrieved_suite=retrieved_suite, suite=suite
    )

    return updated_suite


@router.delete(
    path="/api/v1/suite/{id}",
    response_model=DeleteSuiteResponseModel,
    status_code=200,
)
def delete_suite(*, session: Session = Depends(get_session), id: int) -> Suite | None:
    """Deletes suite."""

    retrieved_suite = retrieve_by_id(session=session, id=id)

    if not retrieved_suite:
        raise SuiteNotFoundException

    deleted_suite = delete(session=session, retrieved_suite=retrieved_suite)

    return deleted_suite
