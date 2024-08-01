from typing import Sequence, List
from sqlmodel import Session
from fastapi import APIRouter, Depends, Query
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

import src.testgate.user.service as user_service
import src.testgate.role.service as role_service

from src.testgate.user.exceptions import (
    InvalidAccessTokenException,
    UserNotFoundByIdException,
    UserNotFoundByEmailException,
    UserUsernameAlreadyExistsException,
    UserEmailAlreadyExistsException,
    InvalidPasswordException,
    InvalidPasswordConfirmationException,
)
from src.testgate.user.models import User

from src.testgate.user.schemas import (
    RetrieveUserResponseModel,
    RetrieveCurrentUserResponseModel,
    UserQueryParametersModel,
    CreateUserResponseModel,
    UpdateUserResponseModel,
    VerifyUserResponseModel,
    ChangeUserPasswordRequestModel,
    ChangeUserPasswordResponseModel,
    DeleteUserResponseModel,
    DeleteCurrentUserResponseModel,
    CreateUserRequestModel,
    UpdateUserRequestModel,
)

from config import Settings, get_settings
from src.testgate.database.service import get_sqlmodel_session

from src.testgate.auth.oauth2.token.access import AccessToken
from src.testgate.auth.oauth2.token.refresh import RefreshToken

settings = Settings()
access_token = AccessToken(algorithm=settings.testgate_jwt_access_token_algorithm)
refresh_token = RefreshToken(algorithm=settings.testgate_jwt_refresh_token_algorithm)

router = APIRouter(tags=["users"])


@router.get(
    path="/api/v1/me",
    response_model=RetrieveCurrentUserResponseModel,
    status_code=200,
    summary="Retrieves current user",
)
async def retrieve_current_user(
    *,
    sqlmodel_session: Session = Depends(get_sqlmodel_session),
    settings: Settings = Depends(get_settings),
    http_authorization: HTTPAuthorizationCredentials = Depends(HTTPBearer()),
) -> User:
    """Retrieves current user."""

    verified, payload, headers, signature = access_token.verify_and_decode(
        key=settings.testgate_jwt_access_token_key, token=http_authorization.credentials
    )

    if not verified:
        raise InvalidAccessTokenException

    retrieved_user = await user_service.retrieve_by_email(
        sqlmodel_session=sqlmodel_session, user_email=payload["email"]
    )

    if not retrieved_user:
        raise UserNotFoundByEmailException

    return retrieved_user


@router.get(
    path="/api/v1/users/{user_id}",
    response_model=RetrieveUserResponseModel,
    status_code=200,
    summary="Retrieves user by id",
)
async def retrieve_user_by_id(
    *, user_id: int, sqlmodel_session: Session = Depends(get_sqlmodel_session)
) -> User:
    """Retrieves user by id."""

    retrieved_user = await user_service.retrieve_by_id(
        sqlmodel_session=sqlmodel_session, user_id=user_id
    )

    if not retrieved_user:
        raise UserNotFoundByIdException

    return retrieved_user


@router.get(
    path="/api/v1/users",
    response_model=List[RetrieveUserResponseModel],
    status_code=200,
    summary="Retrieves user by query parameters",
)
async def retrieve_user_by_query_parameters(
    *,
    sqlmodel_session: Session = Depends(get_sqlmodel_session),
    offset: int = 0,
    limit: int = Query(default=100, lte=100),
    firstname: str = Query(default=None),
    lastname: str = Query(default=None),
    username: str = Query(default=None),
    email: str = Query(default=None),
    verified: bool = Query(default=False),
    role: str = Query(default=None),
) -> Sequence[User]:
    """Retrieves user by query parameters."""

    query_parameters = UserQueryParametersModel(
        offset=offset,
        limit=limit,
        firstname=firstname,
        lastname=lastname,
        username=username,
        email=email,
        verified=verified,
        role=role,
    )

    retrieved_user = await user_service.retrieve_by_query_parameters(
        sqlmodel_session=sqlmodel_session, query_parameters=query_parameters
    )

    return retrieved_user


@router.post(
    path="/api/v1/users",
    response_model=CreateUserResponseModel,
    status_code=201,
    summary="Creates user",
)
async def create_user(
    *,
    sqlmodel_session: Session = Depends(get_sqlmodel_session),
    user: CreateUserRequestModel,
) -> User:
    """Creates user."""

    retrieved_user = await user_service.retrieve_by_username(
        sqlmodel_session=sqlmodel_session, user_username=user.username
    )

    if retrieved_user:
        raise UserUsernameAlreadyExistsException

    retrieved_user = await user_service.retrieve_by_email(
        sqlmodel_session=sqlmodel_session, user_email=user.email
    )

    if retrieved_user:
        raise UserEmailAlreadyExistsException

    created_user = await user_service.create(
        sqlmodel_session=sqlmodel_session, user=user
    )

    return created_user


@router.put(
    path="/api/v1/me",
    response_model=UpdateUserResponseModel,
    status_code=200,
    summary="Updates current user",
)
async def update_current_user(
    *,
    user: UpdateUserRequestModel,
    sqlmodel_session: Session = Depends(get_sqlmodel_session),
    retrieved_user: User = Depends(retrieve_current_user),
) -> User:
    """Updates current user."""

    user.role = await role_service.retrieve_by_name(
        sqlmodel_session=sqlmodel_session, name=user.role.name
    )

    updated_user = await user_service.update(
        sqlmodel_session=sqlmodel_session, retrieved_user=retrieved_user, user=user
    )

    return updated_user


@router.put(
    path="/api/v1/users/{user_id}",
    response_model=UpdateUserResponseModel,
    status_code=200,
    summary="Updates user by id",
)
async def update_user(
    *,
    user_id: int,
    user: UpdateUserRequestModel,
    sqlmodel_session: Session = Depends(get_sqlmodel_session),
) -> User:
    """Updates user."""

    retrieved_user = await user_service.retrieve_by_id(
        sqlmodel_session=sqlmodel_session, user_id=user_id
    )

    if not retrieved_user:
        raise UserNotFoundByIdException

    user.role = await role_service.retrieve_by_name(
        sqlmodel_session=sqlmodel_session, name=user.role.name
    )

    updated_user = await user_service.update(
        sqlmodel_session=sqlmodel_session, retrieved_user=retrieved_user, user=user
    )

    return updated_user


@router.get(
    path="/api/v1/users/email/verify/{token}",
    response_model=VerifyUserResponseModel,
    status_code=200,
)
async def verify_current_user(
    *,
    token: str,
    sqlmodel_session: Session = Depends(get_sqlmodel_session),
    settings: Settings = Depends(get_settings),
) -> User:
    """Verifies current user."""

    verified, payload, headers, signature = access_token.verify_and_decode(
        key=settings.testgate_jwt_access_token_key,
        token=token,
    )

    if not verified:
        raise InvalidAccessTokenException

    retrieved_user = await user_service.retrieve_by_email(
        sqlmodel_session=sqlmodel_session, user_email=payload["email"]
    )

    if not retrieved_user:
        raise UserNotFoundByEmailException

    verified_user = await user_service.verify(
        sqlmodel_session=sqlmodel_session, retrieved_user=retrieved_user
    )

    return verified_user


@router.put(
    path="/api/v1/me/change-password",
    response_model=ChangeUserPasswordResponseModel,
    status_code=201,
)
async def update_current_user_password(
    *,
    sqlmodel_session: Session = Depends(get_sqlmodel_session),
    change_password: ChangeUserPasswordRequestModel,
    retrieved_user: User = Depends(retrieve_current_user),
) -> User:
    """Updates current user password."""

    if not retrieved_user.check_password(change_password.current_password):
        raise InvalidPasswordException

    if change_password.password != change_password.password_confirmation:
        raise InvalidPasswordConfirmationException

    updated_user = await user_service.update_password(
        sqlmodel_session=sqlmodel_session,
        retrieved_user=retrieved_user,
        password=change_password.password,
    )

    return updated_user


# @router.get(path="/api/v1/user/email/verification/{token}", status_code=200)
# def send_user_verification_email(
#     *,
#     token: str,
#     settings: Settings = Depends(get_settings),
#     email_service: EmailService = Depends(get_email_service),
# ):
#     verified, payload, headers, signature = access_token.verify_and_decode(
#         key=settings.testgate_jwt_access_token_key,
#         token=token,
#     )
#
#     if not verified:
#         raise InvalidAccessTokenException
#
#     email_service.email_subject = "Email Verification"
#     email_service.email_to = payload["email"]
#
#     email_service.add_plain_text_message(
#         "Hi!\nHow are you?\nHere is the link you wanted:\nhttp://www.python.org"
#     )
#     email_service.add_html_message(
#         """\
#             <html>
#                 <head></head>
#                 <body>
#                     <p>
#                         Hi!
#                         <br>How are you?<br>
#                         Here is the <a href="http://www.python.org">link</a> you wanted.
#                     </p>
#                 </body>
#             </html>
#         """
#     )
#     email_service.start_smtp_server()
#     email_service.send_email()


@router.delete(
    path="/api/v1/me",
    response_model=DeleteCurrentUserResponseModel,
    status_code=200,
    summary="Deletes current user",
)
async def delete_current_user(
    *,
    sqlmodel_session: Session = Depends(get_sqlmodel_session),
    retrieved_user: User = Depends(retrieve_current_user),
) -> User:
    """Deletes current user."""

    deleted_user = await user_service.delete(
        sqlmodel_session=sqlmodel_session, retrieved_user=retrieved_user
    )

    return deleted_user


@router.delete(
    path="/api/v1/users/{user_id}",
    response_model=DeleteUserResponseModel,
    status_code=200,
    summary="Deletes user",
)
async def delete_user(
    *, user_id: int, sqlmodel_session: Session = Depends(get_sqlmodel_session)
) -> User:
    """Deletes user."""

    retrieved_user = await user_service.retrieve_by_id(
        sqlmodel_session=sqlmodel_session, user_id=user_id
    )

    if not retrieved_user:
        raise UserNotFoundByIdException

    deleted_user = await user_service.delete(
        sqlmodel_session=sqlmodel_session, retrieved_user=retrieved_user
    )

    return deleted_user
