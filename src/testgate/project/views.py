import smtplib
from sqlmodel import Session
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from .service import *
from .schemas import *
from ..user.views import allow_create_resource

from ..database.database import get_session

router = APIRouter(tags=["projects"])

ProjectNotFoundException = HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                         detail="A project with this id does not exist")

ProjectAlreadyExistsException = HTTPException(status_code=status.HTTP_409_CONFLICT,
                                              detail="A project with this id already exists")


@router.get(path="/api/v1/project/{id}",
            response_model=RetrieveProjectResponseModel,
            status_code=200,
            dependencies=[Depends(allow_create_resource)])
def retrieve_project_by_id(*, session: Session = Depends(get_session), id: int):
    """Retrieves project by id."""

    retrieved_project = retrieve_by_id(session=session, id=id)

    if not retrieved_project:
        raise ProjectNotFoundException

    return retrieved_project


@router.get(path="/api/v1/projects",
            response_model=List[RetrieveProjectResponseModel],
            status_code=200,
            dependencies=[Depends(allow_create_resource)])
def retrieve_project_by_query_parameters(*, session: Session = Depends(get_session), name: str = None):
    """Retrieve project by name"""

    retrieved_project = retrieve_by_query_parameters(session=session, query_parameters={"name": name})

    return retrieved_project


@router.post(path="/api/v1/project",
             response_model=CreateProjectResponseModel,
             status_code=201,
             dependencies=[Depends(allow_create_resource)])
def create_project(*, session: Session = Depends(get_session), project: CreateProjectRequestModel):
    """Create project"""

    retrieved_project = retrieve_by_name(session=session, name=project.name)

    if retrieved_project:
        raise ProjectAlreadyExistsException

    created_project = create(session=session, project=project)

    return created_project


@router.put(path="/api/v1/project/{id}",
            response_model=UpdateProjectResponseModel,
            status_code=200,
            dependencies=[Depends(allow_create_resource)])
def update_project(*, session: Session = Depends(get_session), id: int, project: UpdateProjectRequestModel):
    """Update project"""

    retrieved_project = retrieve_by_id(session=session, id=id)

    if not retrieved_project:
        raise ProjectNotFoundException

    updated_project = update(session=session, retrieved_project=retrieved_project, project=project)

    return updated_project


@router.delete(path="/api/v1/project/{id}",
               response_model=DeleteProjectResponseModel,
               status_code=200,
               dependencies=[Depends(allow_create_resource)])
def delete_project(*, session: Session = Depends(get_session), id: int):
    """Delete project"""

    retrieved_project = retrieve_by_id(session=session, id=id)

    if not retrieved_project:
        raise ProjectNotFoundException

    deleted_project = delete(session=session, retrieved_project=retrieved_project)

    return deleted_project
