import pytest
from pytest_factoryboy import register
from typing import Any, Generator, AsyncGenerator
from fastapi import FastAPI
from fastapi.testclient import TestClient
from redis.asyncio import Redis
from fakeredis import FakeAsyncRedis
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
from src.testgate.database.service import (
    get_redis_client,
    get_sqlmodel_session,
)

from tests.user.conftest import UserFactory
from tests.role.conftest import RoleFactory
from tests.permission.conftest import PermissionFactory
from tests.repository.conftest import RepositoryFactory
from tests.execution.conftest import (
    ExecutionJobFactory,
    ExecutionRunnerFactory,
    ExecutionResultFactory,
    ExecutionFactory,
)
from tests.suite.conftest import SuiteResultFactory, SuiteFactory
from tests.case.conftest import CaseResultFactory, CaseFactory

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    url=SQLALCHEMY_DATABASE_URL, echo=True, connect_args={"check_same_thread": False}
)

register(UserFactory)
register(RoleFactory)
register(PermissionFactory)
register(RepositoryFactory)
register(ExecutionJobFactory)
register(ExecutionRunnerFactory)
register(ExecutionResultFactory)
register(ExecutionFactory)
register(SuiteResultFactory)
register(SuiteFactory)
register(CaseResultFactory)
register(CaseFactory)


@pytest.fixture(autouse=True)
async def set_session_for_factory(sqlmodel_session):
    UserFactory._meta.sqlalchemy_session = sqlmodel_session
    RoleFactory._meta.sqlalchemy_session = sqlmodel_session
    PermissionFactory._meta.sqlalchemy_session = sqlmodel_session
    RepositoryFactory._meta.sqlalchemy_session = sqlmodel_session
    ExecutionJobFactory._meta.sqlalchemy_session = sqlmodel_session
    ExecutionRunnerFactory._meta.sqlalchemy_session = sqlmodel_session
    ExecutionResultFactory._meta.sqlalchemy_session = sqlmodel_session
    ExecutionFactory._meta.sqlalchemy_session = sqlmodel_session
    SuiteResultFactory._meta.sqlalchemy_session = sqlmodel_session
    SuiteFactory._meta.sqlalchemy_session = sqlmodel_session
    CaseResultFactory._meta.sqlalchemy_session = sqlmodel_session
    CaseFactory._meta.sqlalchemy_session = sqlmodel_session


async def start_application() -> FastAPI | None:
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
async def app() -> AsyncGenerator[FastAPI, Any]:
    SQLModel.metadata.create_all(bind=engine)
    _app = await start_application()
    yield _app
    SQLModel.metadata.drop_all(bind=engine)


@pytest.fixture
async def sqlmodel_session(app: FastAPI) -> AsyncGenerator[Session, Any]:
    connection = engine.connect()
    transaction = connection.begin()
    session = Session(bind=connection)
    yield session
    session.close()
    transaction.rollback()
    connection.close()


@pytest.fixture
async def redis_client(app: FastAPI) -> AsyncGenerator[Redis, Any]:
    client = FakeAsyncRedis()
    yield await client
    await client.aclose()


@pytest.fixture
async def client(
    app: FastAPI, sqlmodel_session: Session, redis_client: Redis
) -> AsyncGenerator[TestClient, Any]:
    def _get_sqlmodel_session() -> Generator[Session, Any, Any]:
        yield sqlmodel_session

    async def _get_redis_client() -> AsyncGenerator[Redis, Any]:
        await redis_client.flushdb()
        yield redis_client

    def _get_settings():
        return Settings(
            testgate_jwt_access_token_exp_minutes="60",
            testgate_jwt_access_token_key="SJ6nWJtM737AZWevVdDEr4Fh0GmoyR8k",
            testgate_jwt_refresh_token_exp_days="90",
            testgate_jwt_refresh_token_key="SJ6nWJtM737AZWevVdDEr4Fh0GmoyR8k",
            testgate_smtp_email_verification=False,
        )

    app.dependency_overrides[get_sqlmodel_session] = _get_sqlmodel_session
    app.dependency_overrides[get_redis_client] = _get_redis_client
    app.dependency_overrides[get_settings] = _get_settings

    with TestClient(app) as client:
        yield client
