from typing import Any
from typing import Generator
from alembic import command
from alembic.config import Config
import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine

from src.testgate.role.schemas import CreateRoleRequestModel
from src.testgate.role.service import upsert_role_service
from src.testgate.auth.schemas import CreateUserRequestModel
from src.testgate.auth.service import upsert_user_service

from src.testgate.auth.schemas import CreateUserRequestModel, AuthenticateUserRequestModel
from src.testgate.auth.views import user_router, allow_create_resource, RoleChecker
from src.testgate.role.views import role_router
from src.testgate.database.database import get_session

from tests.role.test_role_service import role

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

connect_args = {"check_same_thread": False}
engine = create_engine(SQLALCHEMY_DATABASE_URL, echo=True, connect_args=connect_args)
SessionTesting = Session(engine, autocommit=False, autoflush=False)

alembic_cfg = Config()
alembic_cfg.set_main_option("sqlalchemy.url", SQLALCHEMY_DATABASE_URL)
alembic_cfg.set_main_option("script_location", "src/alembic/")
command.upgrade(alembic_cfg, "head")
def start_application():
    app = FastAPI()
    app.include_router(user_router)
    app.include_router(role_router)
    return app


@pytest.fixture
def app() -> Generator[FastAPI, Any, None]:
    SQLModel.metadata.create_all(engine)
    _app = start_application()
    yield _app
    SQLModel.metadata.drop_all(engine)


@pytest.fixture
def db_session(app: FastAPI): # -> Generator[SessionTesting, Any, None]:
    connection = engine.connect()
    transaction = connection.begin()
    session = Session(bind=connection)
    yield session  # use the session in tests.
    session.close()
    transaction.rollback()
    connection.close()


@pytest.fixture
def client(
        app: FastAPI, db_session: SessionTesting
) -> Generator[TestClient, Any, None]:

    # upsert_role_service(session=SessionTesting, role=CreateRoleRequestModel(**{'name': "Admin"}))
    # upsert_user_service(session=SessionTesting, user=CreateUserRequestModel(**{"firstname": "admin",
    #                                                                         "lastname": "admin",
    #                                                                         "email": "admin@admin.com",
    #                                                                         "password": "secret",
    #                                                                         "verified": True,
    #                                                                         "roles": ["Admin"],
    #                                                                         "teams": []}))

    def _get_test_db():
        try:
            yield db_session
        finally:
            pass

    def _get_test_resource():
        return True

    app.dependency_overrides[get_session] = _get_test_db
    app.dependency_overrides[allow_create_resource] = _get_test_resource

    with TestClient(app) as client:
        yield client

# @pytest.fixture(scope="function")
# def create_and_authorize_user(client):
#     """
#     Create a new FastAPI TestClient that uses the `db_session` fixture to override
#     the `get_db` dependency that is injected into routes.
#     """
#
#     createUserRequestModel = CreateUserRequestModel(firstname="abdullah",
#                                                     lastname="deliogullari",
#                                                     email="abdullahdeliogullari@yaani.com",
#                                                     password="19961996DsA&",
#                                                     verified=True,
#                                                     roles=[],
#                                                     teams=[])
#
#     response = client.post("api/v1/user", json=createUserRequestModel.dict())
#
#     authenticateUserRequestModel = AuthenticateUserRequestModel(email="abdullahdeliogullari@yaani.com",
#                                                                 password="19961996DsA&")
#
#     response = client.post("api/v1/user/auth", json=authenticateUserRequestModel.dict())
#
#     return response


# @pytest.fixture(scope="module")
# def normal_user_token_headers(client: TestClient, db_session: Session):
#     return authentication_token_from_email(
#         client=client, email=settings.TEST_USER_EMAIL, db=db_session
#     )
