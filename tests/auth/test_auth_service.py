from src.testgate.auth.service import register

from src.testgate.auth.schemas import RegisterCredentials


def test_register(db_session, user_factory):

    credentials = RegisterCredentials(**user_factory.stub().__dict__)

    created_user = register(session=db_session, credentials=credentials)

    assert created_user.email == credentials.email
