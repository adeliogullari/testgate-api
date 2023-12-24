from sqlmodel import Session
from fastapi import Depends, APIRouter
from .service import retrieve_by_id, create, update, delete
from .exceptions import CaseNotFoundException
from .schemas import (
    RetrieveCaseResponseModel,
    CreateCaseRequestModel,
    CreateCaseResponseModel,
    UpdateCaseRequestModel,
    UpdateCaseResponseModel,
    DeleteCaseResponseModel,
)
from src.testgate.database.service import get_session

router = APIRouter(tags=["cases"])


@router.get(
    path="/api/v1/case/{id}",
    response_model=RetrieveCaseResponseModel,
    status_code=200,
)
def retrieve_suite_by_id(*, session: Session = Depends(get_session), id: int):
    """Retrieve case by id."""

    retrieved_case = retrieve_by_id(session=session, id=id)

    if not retrieved_case:
        raise CaseNotFoundException

    return retrieved_case


@router.post(
    path="/api/v1/case",
    response_model=CreateCaseResponseModel,
    status_code=201,
)
def create_suite(
    *, session: Session = Depends(get_session), case: CreateCaseRequestModel
):
    """Creates case."""

    created_case = create(session=session, case=case)

    return created_case


@router.put(
    path="/api/v1/case/{id}",
    response_model=UpdateCaseResponseModel,
    status_code=200,
)
def update_case(
    *, session: Session = Depends(get_session), id: int, case: UpdateCaseRequestModel
):
    """Updates case."""

    retrieved_case = retrieve_by_id(session=session, id=id)

    if not retrieved_case:
        raise CaseNotFoundException

    updated_case = update(session=session, retrieved_case=retrieved_case, case=case)

    return updated_case


@router.delete(
    path="/api/v1/case/{id}",
    response_model=DeleteCaseResponseModel,
    status_code=200,
)
def delete_suite(*, session: Session = Depends(get_session), id: int):
    """Deletes case."""

    retrieved_case = retrieve_by_id(session=session, id=id)

    if not retrieved_case:
        raise CaseNotFoundException

    deleted_case = delete(session=session, retrieved_case=retrieved_case)

    return deleted_case