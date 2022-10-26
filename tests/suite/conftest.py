import pytest
from src.testgate.suite.models import Suite
from pytest_factoryboy import register
from factory.alchemy import SQLAlchemyModelFactory


class SuiteFactory(SQLAlchemyModelFactory):

    class Meta:
        model = Suite
        sqlalchemy_session = None
        sqlalchemy_session_persistence = "flush"

    name = "MySuite"
    description = "Description"
    result = None


@pytest.fixture(autouse=True)
def set_session_for_suite_factory(db_session):
    SuiteFactory._meta.sqlalchemy_session = db_session


register(SuiteFactory)
