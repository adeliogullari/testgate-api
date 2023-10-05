from typing import List, Annotated
from jose import jwt
from sqlmodel import Session
from fastapi import APIRouter, Depends, Query, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

import src.testgate.user.service as user_service
import src.testgate.role.service as role_service
import src.testgate.team.service as team_service
from config import get_settings, Settings
from .models import *
from .exceptions import (UserNotFoundException,
                         UserAlreadyExistsException,
                         UserEmailNotFoundException,
                         InvalidPasswordException,
                         InvalidPasswordConfirmationException)
from .schemas import (RetrieveUserResponseModel,
                      RetrieveCurrentUserResponseModel,
                      UserQueryParametersModel,
                      CreateUserResponseModel,
                      UpdateUserResponseModel,
                      VerifyUserResponseModel,
                      ChangeUserPasswordRequestModel,
                      ChangeUserPasswordResponseModel,
                      DeleteUserResponseModel,
                      AuthenticateUserRequestModel,
                      AuthenticateUserResponseModel,
                      CreateUserRequestModel,
                      UpdateUserRequestModel)

from .constants import *

from ..database.database import get_session
from ..email import EmailService

from src.testgate.auth.oauth2 import AccessToken, RefreshToken
from src.testgate.auth.crypto.digest.strategy import Blake2bMessageDigestStrategy


access_token = AccessToken(Blake2bMessageDigestStrategy())
refresh_token = RefreshToken(Blake2bMessageDigestStrategy())

router = APIRouter(tags=["users"])


@router.get(path="/api/v1/me",
            response_model=RetrieveCurrentUserResponseModel,
            status_code=200,
            summary="Retrieves current user")
def retrieve_current_user(*,
                          session: Annotated[Session, Depends(get_session)],
                          settings: Annotated[Settings, Depends(get_settings)],
                          http_authorization: Annotated[HTTPAuthorizationCredentials, Depends(HTTPBearer())]):
    """Retrieves current user."""

    verified, payload, headers, signature = access_token.verify_and_decode(key=settings.testgate_jwt_access_token_key,
                                                                           token=http_authorization.credentials)

    retrieved_user = user_service.retrieve_by_email(session=session, email=payload['email'])

    return retrieved_user


@router.get(path="/api/v1/users/{id}",
            response_model=RetrieveUserResponseModel,
            status_code=200,
            summary="Retrieves user by id")
def retrieve_user_by_id(*,
                        session: Session = Depends(get_session),
                        id: int):
    """Retrieves user by id."""

    retrieved_user = user_service.retrieve_by_id(session=session, id=id)

    if not retrieved_user:
        raise UserNotFoundException

    return retrieved_user


@router.get(path="/api/v1/users",
            response_model=List[RetrieveUserResponseModel],
            status_code=200,
            summary="Retrieves user by query parameters")
def retrieve_user_by_query_parameters(*,
                                      session: Session = Depends(get_session),
                                      offset: int = 0,
                                      limit: int = Query(default=100, lte=100),
                                      firstname: str = None,
                                      lastname: str = None,
                                      email: str = None,
                                      role: str = Query(),
                                      team: str = Query()):
    """Retrieves user by query parameters."""

    role = role_service.retrieve_by_name(session=session, name=role.name)
    team = team_service.retrieve_by_name(session=session, name=team.name)

    query_parameters = UserQueryParametersModel(offset=offset,
                                                limit=limit,
                                                firstname=firstname,
                                                lastname=lastname,
                                                email=email,
                                                role=role,
                                                teams=team)

    retrieved_user = user_service.retrieve_by_query_parameters(session=session, query_parameters=query_parameters)

    return retrieved_user


@router.post(path="/api/v1/users",
                  response_model=CreateUserResponseModel,
                  status_code=201)
def create_user(*, session: Session = Depends(get_session), user: CreateUserRequestModel):
    """Create user."""

    retrieved_user = user_service.retrieve_by_email(session=session, email=user.email)

    if retrieved_user:
        raise UserAlreadyExistsException

    # if user.role:
    #     user.role = role_service.retrieve_by_name(session=session, name=user.role.name)
    # if user.team:
    #     user.team = team_service.retrieve_by_name(session=session, name=user.team.name)

    created_user = user_service.create(session=session, user=user)

    return created_user


@router.put(path="/api/v1/user/{id}",
                 response_model=UpdateUserResponseModel,
                 status_code=200)
def update_user(*, session: Session = Depends(get_session), id: int, user: UpdateUserRequestModel):
    retrieved_user = user_service.retrieve_by_id(session=session, id=id)

    if not retrieved_user:
        raise UserNotFoundException

    user.role = role_service.retrieve_by_name(session=session, name=user.role.name)
    user.team = team_service.retrieve_by_name(session=session, name=user.team.name)

    updated_user = user_service.update(session=session, retrieved_user=retrieved_user, user=user)

    return updated_user


@router.put(path="/api/v1/users/me",
                 response_model=UpdateUserResponseModel,
                 status_code=200)
def update_current_user(*,
                        session: Session = Depends(get_session),
                        user: UpdateUserRequestModel,
                        http_authorization_credentials: HTTPAuthorizationCredentials = Depends(HTTPBearer()),
                        settings: Annotated[Settings, Depends(get_settings)]):
    """Update current user by token."""

    is_token_verified = access_token.verify(key='key', token=http_authorization_credentials.credentials)

    payload = None
    if is_token_verified:
        payload = access_token.decode(token=http_authorization_credentials.credentials)

    email = payload[0].get('email')

    retrieved_user = user_service.retrieve_by_email(session=session, email=email)

    user.role = role_service.retrieve_by_name(session=session, name=user.role.name)
    user.team = team_service.retrieve_by_name(session=session, name=user.team.name)

    updated_user = user_service.update(session=session, retrieved_user=retrieved_user, user=user)

    return updated_user


@router.put(path="/api/v1/me/change-password/",
            response_model=ChangeUserPasswordResponseModel,
            status_code=201)
def change_current_user_password(*,
                                 session: Session = Depends(get_session),
                                 change_password: ChangeUserPasswordRequestModel,
                                 http_authorization_credentials: HTTPAuthorizationCredentials = Depends(HTTPBearer()),
                                 settings: Annotated[Settings, Depends(get_settings)]):

    is_token_verified = access_token.verify(key='key', token=http_authorization_credentials.credentials)

    payload = None
    if is_token_verified:
        payload = access_token.decode(token=http_authorization_credentials.credentials)

    email = payload[0].get('email')

    retrieved_user = user_service.retrieve_by_email(session=session, email=email)

    if not retrieved_user:
        raise UserEmailNotFoundException

    if not retrieved_user.check_password(change_password.current_password):
        raise InvalidPasswordException

    if not change_password.password == change_password.password_confirmation:
        raise InvalidPasswordConfirmationException

    updated_user = user_service.update_password(session=session,
                                                retrieved_user=retrieved_user,
                                                password=change_password.password)

    return updated_user


@router.get(path="/api/v1/user/email/verify/{token}",
                 response_model=VerifyUserResponseModel,
                 status_code=200)
def verify_current_user(*,
                        session: Session = Depends(get_session),
                        token: str,
                        settings: Annotated[Settings, Depends(get_settings)]):

    is_token_verified = access_token.verify(key='key', token=token)

    payload = None
    if is_token_verified:
        payload = access_token.decode(token=token)

    email = payload[0].get('email')

    retrieved_user = user_service.retrieve_by_email(session=session, email=email)

    if not retrieved_user:
        raise UserNotFoundException

    verified_user = user_service.verify(session=session, retrieved_user=retrieved_user)

    return verified_user


@router.get(path="/api/v1/user/email/verification/{token}",
                 status_code=202)
def send_user_verification_email(*, token, settings: Annotated[Settings, Depends(get_settings)]):
    payload = jwt.decode(token=token, key=JWT_TOKEN_KEY, algorithms=JWT_ACCESS_TOKEN_ALG)
    email = payload.get("email")

    email_service = EmailService()
    email_service.email_subject = "Email Verification"
    email_service.email_from = settings.testgate_smtp_email_address
    email_service.email_to = email
    email_service.email_password = settings.testgate_smtp_email_app_password

    email_service.add_plain_text_message("Hi!\nHow are you?\nHere is the link you wanted:\nhttp://www.python.org")
    email_service.add_html_message(
        """\
            <html>
                <head></head>
                <body>
                    <p>
                        Hi!
                        <br>How are you?<br>
                        Here is the <a href="http://www.python.org">link</a> you wanted.
                    </p>
                </body>
            </html>
        """)
    email_service.start_smtp_server()
    email_service.send_email()


@router.post(path="/api/v1/user/auth",
                  response_model=AuthenticateUserResponseModel,
                  status_code=200)
def authenticate_user(*,
                      session: Session = Depends(get_session),
                      authentication: AuthenticateUserRequestModel):
    retrieved_user = user_service.retrieve_by_email(session=session, email=authentication.email)

    if not retrieved_user:
        raise UserEmailNotFoundException

    if not retrieved_user.check_password(authentication.password):
        raise InvalidPasswordException

    return retrieved_user


@router.delete(path="/api/v1/user/me",
                    response_model=DeleteUserResponseModel,
                    status_code=200)
def delete_current_user_by_token(*,
                                 session: Session = Depends(get_session),
                                 http_authorization_credentials: HTTPAuthorizationCredentials = Depends(HTTPBearer()),
                                 settings: Annotated[Settings, Depends(get_settings)]):
    is_token_verified = access_token.verify(key='key', token=http_authorization_credentials.credentials)

    payload = None
    if is_token_verified:
        payload = access_token.decode(token=http_authorization_credentials.credentials)

    email = payload[0].get('email')

    retrieved_user = user_service.retrieve_by_email(session=session, email=email)

    if not retrieved_user:
        raise UserNotFoundException

    deleted_user = user_service.delete(session=session, retrieved_user=retrieved_user)

    return deleted_user


@router.delete(path="/api/v1/user/{id}",
                    response_model=DeleteUserResponseModel,
                    status_code=200)
def delete_user(*, session: Session = Depends(get_session), id: int):
    retrieved_user = user_service.retrieve_by_id(session=session, id=id)

    if not retrieved_user:
        raise UserNotFoundException

    deleted_user = user_service.delete(session=session, retrieved_user=retrieved_user)

    return deleted_user


@router.get(path="/api/v1/users/me",
                 response_model=RetrieveCurrentUserResponseModel,
                 status_code=200)
def retrieve_current_user_by_token(*,
                                   session: Session = Depends(get_session),
                                   http_authorization_credentials: HTTPAuthorizationCredentials = Depends(
                                       HTTPBearer()),
                                   settings: Annotated[Settings, Depends(get_settings)]):
    """Retrieves current user by access token."""

    is_token_verified = access_token.verify(key='key', token=http_authorization_credentials.credentials)

    payload = None
    if is_token_verified:
        payload = access_token.decode(token=http_authorization_credentials.credentials)

    email = payload[0].get('email')

    retrieved_user = user_service.retrieve_by_email(session=session, email=email)

    return retrieved_user


class RoleChecker:
    def __init__(self, role: str):
        self.role = role

    def __call__(self, current_user: User = Depends(retrieve_current_user)):
        if current_user.role != self.role:
            raise HTTPException(status_code=403, detail="Operation not permitted")


allow_create_resource = RoleChecker("admin")
