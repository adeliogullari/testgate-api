import pytest
from pytest_factoryboy import register
from typing import Any, Generator
from fastapi import FastAPI
from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine
from config import Settings, get_settings

from src.testgate.user.views import allow_create_resource

from src.testgate.auth.views import router as auth_router
from src.testgate.user.views import router as user_router
from src.testgate.role.views import router as role_router
from src.testgate.permission.views import router as permission_router
from src.testgate.repository.views import router as repository_router
from src.testgate.execution.views import router as execution_router
from src.testgate.suite.views import router as suite_router
from src.testgate.case.views import router as case_router
from src.testgate.database.database import get_session

from .user.conftest import UserFactory
from .role.conftest import RoleFactory
from .permission.conftest import PermissionFactory
from .repository.conftest import RepositoryFactory
from .execution.conftest import ExecutionFactory
from .suite.conftest import SuiteFactory

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    url=SQLALCHEMY_DATABASE_URL, echo=True, connect_args={"check_same_thread": False}
)
SessionTesting = Session(engine, autocommit=False, autoflush=False)


@pytest.fixture(autouse=True)
def set_session_for_factory(db_session):
    UserFactory._meta.sqlalchemy_session = db_session
    RoleFactory._meta.sqlalchemy_session = db_session
    PermissionFactory._meta.sqlalchemy_session = db_session
    RepositoryFactory._meta.sqlalchemy_session = db_session


register(UserFactory)
register(RoleFactory)
register(PermissionFactory)
register(RepositoryFactory)
register(ExecutionFactory)
register(SuiteFactory)


def start_application():
    app = FastAPI()
    app.include_router(auth_router)
    app.include_router(user_router)
    app.include_router(role_router)
    app.include_router(permission_router)
    app.include_router(repository_router)
    app.include_router(execution_router)
    app.include_router(suite_router)
    app.include_router(case_router)
    return app


@pytest.fixture
def app() -> Generator[FastAPI, Any, None]:
    SQLModel.metadata.create_all(engine)
    _app = start_application()
    yield _app
    SQLModel.metadata.drop_all(engine)


@pytest.fixture
def db_session(app: FastAPI):
    connection = engine.connect()
    transaction = connection.begin()
    session = Session(bind=connection)
    yield session
    session.close()
    transaction.rollback()
    connection.close()


@pytest.fixture
def client(app: FastAPI, db_session: SessionTesting):
    def _get_session():
        try:
            yield db_session
        finally:
            pass

    def _get_settings():
        return Settings(
            testgate_jwt_access_token_exp_minutes="60",
            testgate_jwt_access_token_key="SJ6nWJtM737AZWevVdDEr4Fh0GmoyR8k",
            testgate_jwt_refresh_token_exp_days="90",
            testgate_jwt_refresh_token_key="SJ6nWJtM737AZWevVdDEr4Fh0GmoyR8k",
        )

    def _allow_create_resource():
        return True

    app.dependency_overrides[get_session] = _get_session
    app.dependency_overrides[allow_create_resource] = _allow_create_resource
    app.dependency_overrides[get_settings] = _get_settings

    with TestClient(app) as client:
        yield client
