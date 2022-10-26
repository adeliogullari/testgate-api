from glob import glob
from typing import Any
from typing import Generator
from alembic import command
from alembic.config import Config
import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine

from config import Settings, get_settings
# from src.testgate.role.schemas import CreateRoleRequestModel
# from src.testgate.role.service import upsert_role_service
# from src.testgate.user.schemas import CreateUserRequestModel
# from src.testgate.user.service import upsert_user_service

# from src.testgate.user.schemas import CreateUserRequestModel, AuthenticateUserRequestModel
from src.testgate.auth.views import router as auth_router
from src.testgate.user.views import router as user_router
from src.testgate.user.views import allow_create_resource, RoleChecker
from src.testgate.role.views import role_router
from src.testgate.team.views import team_router
from src.testgate.project.views import project_router
# from src.testgate.plan.views import plan_router
from src.testgate.run.views import run_router
from src.testgate.suite.views import suite_router
# from src.testgate.result.views import result_router
from src.testgate.database.database import get_session

# from .role.conftest import role_factory, role_kwargs, make_role, role
# from .team.conftest import team_factory, team_kwargs, make_team, team
# from .project.conftest import project_kwargs, make_project, project
from .role.conftest import *
from .team.conftest import *
from .user.conftest import *
register(RoleFactory)

# from tests.role.test_role_service import role

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

connect_args = {"check_same_thread": False}
engine = create_engine(SQLALCHEMY_DATABASE_URL, echo=True, connect_args=connect_args)
SessionTesting = Session(engine, autocommit=False, autoflush=False)


# alembic_cfg = Config()
# alembic_cfg.set_main_option("sqlalchemy.url", SQLALCHEMY_DATABASE_URL)
# alembic_cfg.set_main_option("script_location", "src/alembic/")
# command.upgrade(alembic_cfg, "head")


def start_application():
    app = FastAPI()
    app.include_router(auth_router)
    app.include_router(user_router)
    app.include_router(role_router)
    app.include_router(team_router)
    app.include_router(project_router)
    # app.include_router(plan_router)
    app.include_router(run_router)
    app.include_router(suite_router)
    # app.include_router(result_router)
    return app


@pytest.fixture
def app() -> Generator[FastAPI, Any, None]:
    SQLModel.metadata.create_all(engine)
    _app = start_application()
    yield _app
    SQLModel.metadata.drop_all(engine)


@pytest.fixture
def db_session(app: FastAPI):  # -> Generator[SessionTesting, Any, None]:
    connection = engine.connect()
    transaction = connection.begin()
    session = Session(bind=connection)
    yield session
    session.close()
    transaction.rollback()
    connection.close()


@pytest.fixture
def client(app: FastAPI, db_session: SessionTesting):  # -> Generator[TestClient, Any, None]:

    def _get_session():
        try:
            yield db_session
        finally:
            pass

    def _get_settings():
        return Settings(testgate_jwt_token_exp='72000',
                        testgate_jwt_token_key='token_key',
                        testgate_jwt_token_algorithms='HS256')

    def _allow_create_resource():
        return True

    app.dependency_overrides[get_session] = _get_session
    app.dependency_overrides[allow_create_resource] = _allow_create_resource
    app.dependency_overrides[get_settings] = _get_settings

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
#     response = client.post("api/v1/user/user", json=authenticateUserRequestModel.dict())
#
#     return response


# @pytest.fixture(scope="module")
# def normal_user_token_headers(client: TestClient, db_session: Session):
#     return authentication_token_from_email(
#         client=client, email=settings.TEST_USER_EMAIL, db=db_session
#     )
