from sqlmodel import Session
from src.testgate.suite.models import Suite
from tests.suite.conftest import SuiteFactory
from src.testgate.suite.service import create, retrieve_by_id, retrieve_by_name


async def test_create(sqlmodel_session: Session, suite_factory: SuiteFactory) -> None:
    suite = suite_factory.stub()

    created_suite = await create(sqlmodel_session=sqlmodel_session, suite=suite)

    assert created_suite.name == created_suite.name


async def test_retrieve_by_id(sqlmodel_session: Session, suite: Suite) -> None:
    retrieved_suite = await retrieve_by_id(
        sqlmodel_session=sqlmodel_session, id=suite.id
    )

    assert retrieved_suite.id == suite.id


async def test_retrieve_by_name(sqlmodel_session: Session, suite: Suite) -> None:
    retrieved_suite = await retrieve_by_name(
        sqlmodel_session=sqlmodel_session, name=suite.name
    )

    assert retrieved_suite.id == suite.id
