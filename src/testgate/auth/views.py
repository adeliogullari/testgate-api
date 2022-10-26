from typing import List, Annotated
from jose import jwt
from sqlmodel import Session
from fastapi import APIRouter, Depends, HTTPException, status, Query
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

import src.testgate.user.service as user_service
import src.testgate.role.service as role_service
import src.testgate.team.service as team_service
from config import get_settings, Settings
# from .models import *
# from .exceptions import *
from .schemas import AuthLoginRequestModel, \
    AuthLoginResponseModel, \
    AuthRegisterRequestModel, \
    AuthRegisterResponseModel
from src.testgate.user.exceptions import *
# from .constants import *

from fastapi import HTTPException
from starlette.status import HTTP_403_FORBIDDEN, \
    HTTP_404_NOT_FOUND, \
    HTTP_409_CONFLICT

from ..database.database import get_session

router = APIRouter(tags=["auth"])


@router.post(path="/api/v1/auth/login",
             response_model=AuthLoginResponseModel,
             status_code=200)
def login(*,
          session: Session = Depends(get_session),
          login_credentials: AuthLoginRequestModel):

    retrieved_user = user_service.retrieve_by_email(session=session, email=login_credentials.email)

    if not retrieved_user:
        raise UserEmailNotFoundException

    if not retrieved_user.check_password(login_credentials.password):
        raise InvalidPasswordException

    return retrieved_user


@router.post(path="/api/v1/auth/register",
             response_model=AuthRegisterResponseModel,
             status_code=200)
def register(*,
             session: Session = Depends(get_session),
             register_credentials: AuthRegisterRequestModel):
    retrieved_user = user_service.retrieve_by_email(session=session, email=register_credentials.email)

    if retrieved_user:
        raise UserAlreadyExistsException

    # if user.role:
    #     user.role = role_service.retrieve_by_name(session=session, name=user.role.name)
    # if user.team:
    #     user.team = team_service.retrieve_by_name(session=session, name=user.team.name)

    # created_user = user_service.create(session=session, user=register_credentials)
    #
    # return created_user

    return None
