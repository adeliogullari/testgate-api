from typing import List
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
from src.testgate.database.service import get_session
# from src.testgate.email.service import EmailService, get_email_service

from src.testgate.auth.oauth2.token.access import AccessToken
from src.testgate.auth.oauth2.token.refresh import RefreshToken
from src.testgate.auth.crypto.digest.strategy import Blake2bMessageDigestStrategy

access_token = AccessToken(Blake2bMessageDigestStrategy())
refresh_token = RefreshToken(Blake2bMessageDigestStrategy())

router = APIRouter(tags=["users"])


@router.get(
    path="/api/v1/me",
    response_model=RetrieveCurrentUserResponseModel,
    status_code=200,
    summary="Retrieves current user",
)
def retrieve_current_user(
    *,
    session: Session = Depends(get_session),
    settings: Settings = Depends(get_settings),
    http_authorization: HTTPAuthorizationCredentials = Depends(HTTPBearer()),
) -> User:
    """Retrieves current user."""

    verified, payload, headers, signature = access_token.verify_and_decode(
        key=settings.testgate_jwt_access_token_key, token=http_authorization.credentials
    )

    if not verified:
        raise InvalidAccessTokenException

    retrieved_user = user_service.retrieve_by_email(
        session=session, user_email=payload["email"]
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
def retrieve_user_by_id(
    *, user_id: int, session: Session = Depends(get_session)
) -> User:
    """Retrieves user by id."""

    retrieved_user = user_service.retrieve_by_id(session=session, user_id=user_id)

    if not retrieved_user:
        raise UserNotFoundByIdException

    return retrieved_user


@router.get(
    path="/api/v1/users",
    response_model=List[RetrieveUserResponseModel],
    status_code=200,
    summary="Retrieves user by query parameters",
)
def retrieve_user_by_query_parameters(
    *,
    session: Session = Depends(get_session),
    offset: int = 0,
    limit: int = Query(default=100, lte=100),
    firstname: str = Query(default=None),
    lastname: str = Query(default=None),
    username: str = Query(default=None),
    email: str = Query(default=None),
    verified: bool = Query(default=False),
    role: str = Query(default=None),
) -> list[User] | None:
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

    retrieved_user = user_service.retrieve_by_query_parameters(
        session=session, query_parameters=query_parameters
    )

    return retrieved_user


@router.post(
    path="/api/v1/users",
    response_model=CreateUserResponseModel,
    status_code=201,
    summary="Creates user",
)
def create_user(
    *, session: Session = Depends(get_session), user: CreateUserRequestModel
) -> User | None:
    """Creates user."""

    retrieved_user = user_service.retrieve_by_username(
        session=session, user_username=user.username
    )

    if retrieved_user:
        raise UserUsernameAlreadyExistsException

    retrieved_user = user_service.retrieve_by_email(
        session=session, user_email=user.email
    )

    if retrieved_user:
        raise UserEmailAlreadyExistsException

    user.role = role_service.retrieve_by_name(session=session, name=user.role.name)

    created_user = user_service.create(session=session, user=user)

    return created_user


@router.put(
    path="/api/v1/me",
    response_model=UpdateUserResponseModel,
    status_code=200,
    summary="Updates current user",
)
def update_current_user(
    *,
    user: UpdateUserRequestModel,
    session: Session = Depends(get_session),
    retrieved_user: User = Depends(retrieve_current_user),
) -> User | None:
    """Updates current user."""

    user.role = role_service.retrieve_by_name(session=session, name=user.role.name)

    updated_user = user_service.update(
        session=session, retrieved_user=retrieved_user, user=user
    )

    return updated_user


@router.put(
    path="/api/v1/users/{user_id}",
    response_model=UpdateUserResponseModel,
    status_code=200,
    summary="Updates user by id",
)
def update_user(
    *,
    user_id: int,
    user: UpdateUserRequestModel,
    session: Session = Depends(get_session),
) -> User | None:
    """Updates user."""

    retrieved_user = user_service.retrieve_by_id(session=session, user_id=user_id)

    if not retrieved_user:
        raise UserNotFoundByIdException

    user.role = role_service.retrieve_by_name(session=session, name=user.role.name)

    updated_user = user_service.update(
        session=session, retrieved_user=retrieved_user, user=user
    )

    return updated_user


@router.get(
    path="/api/v1/users/email/verify/{token}",
    response_model=VerifyUserResponseModel,
    status_code=200,
)
def verify_current_user(
    *,
    token: str,
    session: Session = Depends(get_session),
    settings: Settings = Depends(get_settings),
) -> User | None:
    """Verifies current user."""

    verified, payload, headers, signature = access_token.verify_and_decode(
        key=settings.testgate_jwt_access_token_key,
        token=token,
    )

    if not verified:
        raise InvalidAccessTokenException

    retrieved_user = user_service.retrieve_by_email(
        session=session, user_email=payload["email"]
    )

    if not retrieved_user:
        raise UserNotFoundByEmailException

    verified_user = user_service.verify(session=session, retrieved_user=retrieved_user)

    return verified_user


@router.put(
    path="/api/v1/me/change-password",
    response_model=ChangeUserPasswordResponseModel,
    status_code=201,
)
def update_current_user_password(
    *,
    session: Session = Depends(get_session),
    change_password: ChangeUserPasswordRequestModel,
    retrieved_user: User = Depends(retrieve_current_user),
) -> User | None:
    """Updates current user password."""

    if not retrieved_user.check_password(change_password.current_password):
        raise InvalidPasswordException

    if change_password.password != change_password.password_confirmation:
        raise InvalidPasswordConfirmationException

    updated_user = user_service.update_password(
        session=session,
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
def delete_current_user(
    *,
    session: Session = Depends(get_session),
    retrieved_user: User = Depends(retrieve_current_user),
) -> User | None:
    """Deletes current user."""

    deleted_user = user_service.delete(session=session, retrieved_user=retrieved_user)

    return deleted_user


@router.delete(
    path="/api/v1/users/{user_id}",
    response_model=DeleteUserResponseModel,
    status_code=200,
    summary="Deletes user",
)
def delete_user(
    *, user_id: int, session: Session = Depends(get_session)
) -> User | None:
    """Deletes user."""

    retrieved_user = user_service.retrieve_by_id(session=session, user_id=user_id)

    if not retrieved_user:
        raise UserNotFoundByIdException

    deleted_user = user_service.delete(session=session, retrieved_user=retrieved_user)

    return deleted_user
