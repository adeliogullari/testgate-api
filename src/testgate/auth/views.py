from sqlmodel import Session
from fastapi import APIRouter, Depends
import src.testgate.auth.service as auth_service
import src.testgate.user.service as user_service
from src.testgate.user.models import User
from src.testgate.auth.schemas import (
    LoginCredentials,
    LoginResponse,
    RegisterCredentials,
    RegisterResponse,
)
from src.testgate.user.exceptions import (
    UserNotFoundByEmailException,
    UserIsNotVerifiedException,
    UserEmailAlreadyExistsException,
    InvalidPasswordException,
)
from src.testgate.database.service import get_session
from config import Settings, get_settings

router = APIRouter(tags=["auth"])


@router.post(path="/api/v1/auth/login", response_model=LoginResponse, status_code=200)
def login(
    *, session: Session = Depends(get_session), login_credentials: LoginCredentials
) -> User:
    retrieved_user = user_service.retrieve_by_email(
        session=session, user_email=login_credentials.email
    )

    if not retrieved_user:
        raise UserNotFoundByEmailException

    if not retrieved_user.verified:
        raise UserIsNotVerifiedException

    if not retrieved_user.check_password(password=login_credentials.password):
        raise InvalidPasswordException

    return retrieved_user


@router.post(
    path="/api/v1/auth/register", response_model=RegisterResponse, status_code=200
)
def register(
    *,
    session: Session = Depends(get_session),
    settings: Settings = Depends(get_settings),
    credentials: RegisterCredentials,
) -> User:
    retrieved_user = user_service.retrieve_by_email(
        session=session, user_email=credentials.email
    )

    if retrieved_user:
        raise UserEmailAlreadyExistsException

    created_user = auth_service.register(session=session, credentials=credentials)

    if not settings.testgate_smtp_email_verification:
        created_user = user_service.verify(session=session, retrieved_user=created_user)

    return created_user
