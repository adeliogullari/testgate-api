from sqlmodel import Session
from src.testgate.auth.service import register
from src.testgate.auth.schemas import RegisterCredentials
from tests.user.conftest import UserFactory


async def test_register(sqlmodel_session: Session, user_factory: UserFactory):
    credentials = RegisterCredentials(
        **user_factory.stub(password="password_2024").__dict__
    )

    created_user = await register(
        sqlmodel_session=sqlmodel_session, credentials=credentials
    )

    assert created_user.email == credentials.email
