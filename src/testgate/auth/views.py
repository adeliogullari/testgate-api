from sqlmodel import Session
from fastapi import APIRouter, Depends
import src.testgate.auth.service as auth_service
import src.testgate.user.service as user_service
from src.testgate.email.schema import SendEmail
from src.testgate.email.service import aio_kafka_email_producer
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
from src.testgate.database.service import get_sqlmodel_session
from config import Settings, get_settings

router = APIRouter(tags=["auth"])


@router.post(path="/api/v1/auth/login", response_model=LoginResponse, status_code=200)
async def login(
    *,
    sqlmodel_session: Session = Depends(get_sqlmodel_session),
    settings: Settings = Depends(get_settings),
    credentials: LoginCredentials,
) -> User:
    retrieved_user = await user_service.retrieve_by_email(
        sqlmodel_session=sqlmodel_session, user_email=credentials.email
    )

    if not retrieved_user:
        raise UserNotFoundByEmailException

    if not retrieved_user.verified and settings.testgate_smtp_email_verification:
        raise UserIsNotVerifiedException

    if not retrieved_user.check_password(password=credentials.password):
        raise InvalidPasswordException

    return retrieved_user


@router.post(
    path="/api/v1/auth/register", response_model=RegisterResponse, status_code=200
)
async def register(
    *,
    sqlmodel_session: Session = Depends(get_sqlmodel_session),
    settings: Settings = Depends(get_settings),
    credentials: RegisterCredentials,
) -> User | None:
    retrieved_user = await user_service.retrieve_by_email(
        sqlmodel_session=sqlmodel_session, user_email=credentials.email
    )

    if retrieved_user:
        raise UserEmailAlreadyExistsException

    created_user = await auth_service.register(
        sqlmodel_session=sqlmodel_session, credentials=credentials
    )

    if settings.testgate_smtp_email_verification:
        await aio_kafka_email_producer(
            value=SendEmail(
                subject="Email Verification",
                to_addrs=created_user.email,
                plain_text_message="Email Verification",
                html_message="Email Verification",
            ).model_dump()
        )

    return created_user
