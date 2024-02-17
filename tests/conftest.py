import pytest
from pytest_factoryboy import register
from typing import Any, Generator
from fastapi import FastAPI
from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine
from config import Settings, get_settings

from src.testgate.auth.views import router as auth_router
from src.testgate.user.views import router as user_router
from src.testgate.role.views import router as role_router
from src.testgate.permission.views import router as permission_router
from src.testgate.repository.views import router as repository_router
from src.testgate.execution.views import router as execution_router
from src.testgate.suite.views import router as suite_router
from src.testgate.case.views import router as case_router
from src.testgate.database.service import get_session

from tests.user.conftest import UserFactory
from tests.role.conftest import RoleFactory
from tests.permission.conftest import PermissionFactory
from tests.repository.conftest import RepositoryFactory
from tests.execution.conftest import ExecutionResultFactory, ExecutionFactory
from tests.suite.conftest import SuiteResultFactory, SuiteFactory
from tests.case.conftest import CaseResultFactory, CaseFactory

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    url=SQLALCHEMY_DATABASE_URL, echo=True, connect_args={"check_same_thread": False}
)

SessionTesting = Session(engine, autocommit=False, autoflush=False)

register(UserFactory)
register(RoleFactory)
register(PermissionFactory)
register(RepositoryFactory)
register(ExecutionResultFactory)
register(ExecutionFactory)
register(SuiteResultFactory)
register(SuiteFactory)
register(CaseResultFactory)
register(CaseFactory)


@pytest.fixture(autouse=True)
def set_session_for_factory(db_session):
    UserFactory._meta.sqlalchemy_session = db_session
    RoleFactory._meta.sqlalchemy_session = db_session
    PermissionFactory._meta.sqlalchemy_session = db_session
    RepositoryFactory._meta.sqlalchemy_session = db_session
    ExecutionResultFactory._meta.sqlalchemy_session = db_session
    ExecutionFactory._meta.sqlalchemy_session = db_session
    SuiteResultFactory._meta.sqlalchemy_session = db_session
    SuiteFactory._meta.sqlalchemy_session = db_session
    CaseResultFactory._meta.sqlalchemy_session = db_session
    CaseFactory._meta.sqlalchemy_session = db_session


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
            testgate_smtp_email_verification=False,
        )

    app.dependency_overrides[get_session] = _get_session
    app.dependency_overrides[get_settings] = _get_settings

    with TestClient(app) as client:
        yield client
