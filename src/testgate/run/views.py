from typing import List
from sqlmodel import Session
from fastapi import status, Depends, APIRouter, HTTPException
from .service import retrieve_by_id, retrieve_by_name, retrieve_by_query_parameters, create, update, delete
from .schemas import RetrieveRunResponseModel, \
                     CreateRunRequestModel, \
                     CreateRunResponseModel, \
                     UpdateRunRequestModel, \
                     UpdateRunResponseModel, \
                     DeleteRunResponseModel
from ..user.views import allow_create_resource
from ..database.database import get_session

run_router = APIRouter(tags=["runs"])

RunNotFoundException = HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                     detail="A run with that id does not exist")

RunAlreadyExistsException = HTTPException(status_code=status.HTTP_409_CONFLICT,
                                          detail="A run with that id already exists")


@run_router.get(path="/api/v1/run/{id}",
                response_model=None,
                status_code=200,
                dependencies=[Depends(allow_create_resource)])
def retrieve_run_by_id(*, session: Session = Depends(get_session), id: int):
    """Retrieve run by id."""

    retrieved_run = retrieve_by_id(session=session, id=id)

    if not retrieved_run:
        raise RunNotFoundException

    return retrieved_run


@run_router.get(path="/api/v1/runs",
                response_model=List[RetrieveRunResponseModel],
                status_code=200,
                dependencies=[Depends(allow_create_resource)])
def retrieve_run_by_query_parameters(*, session: Session = Depends(get_session), name: str = None):
    """Search run by name."""

    retrieved_run = retrieve_by_query_parameters(session=session, query_parameters={"name": name})

    return retrieved_run


@run_router.post(path="/api/v1/run",
                 response_model=CreateRunResponseModel,
                 status_code=201,
                 dependencies=[Depends(allow_create_resource)])
def create_run(*, session: Session = Depends(get_session), run: CreateRunRequestModel):
    """Creates run."""

    retrieved_run = retrieve_by_name(session=session, name=run.name)

    if retrieved_run:
        raise RunAlreadyExistsException

    created_run = create(session=session, run=run)

    return created_run


@run_router.put(path="/api/v1/run/{id}",
                response_model=UpdateRunResponseModel,
                status_code=200,
                dependencies=[Depends(allow_create_resource)])
def update_run(*, session: Session = Depends(get_session), id: int, run: UpdateRunRequestModel):
    """Updates run."""

    retrieved_run = retrieve_by_id(session=session, id=id)

    if not retrieved_run:
        raise RunNotFoundException

    updated_run = update(session=session, retrieved_run=retrieved_run, run=run)

    return updated_run


@run_router.delete(path="/api/v1/run/{id}",
                   response_model=DeleteRunResponseModel,
                   status_code=200,
                   dependencies=[Depends(allow_create_resource)])
def delete_run(*, session: Session = Depends(get_session), id: int):
    """Deletes run."""

    retrieved_run = retrieve_by_id(session=session, id=id)

    if not retrieved_run:
        raise RunNotFoundException

    deleted_run = delete(session=session, retrieved_run=retrieved_run)

    return deleted_run


