import pytest
import factory
from src.testgate.suite.models import Suite, SuiteResult
from pytest_factoryboy import register
from factory.alchemy import SQLAlchemyModelFactory


class SuiteResultFactory(SQLAlchemyModelFactory):
    class Meta:
        model = SuiteResult
        sqlalchemy_session = None
        sqlalchemy_session_persistence = "flush"

    total = 0
    passed = 0
    failed = 0
    skipped = 0


class SuiteFactory(SQLAlchemyModelFactory):
    class Meta:
        model = Suite
        sqlalchemy_session = None
        sqlalchemy_session_persistence = "flush"

    name = "MySuite"
    description = "Description"
    result = factory.SubFactory(SuiteResultFactory)

    @factory.post_generation
    def result_generation(self, create, extracted, **kwargs):
        if not create:
            self.result = self.result.__dict__


@pytest.fixture(autouse=True)
def set_session_for_suite_factory(db_session):
    SuiteResultFactory._meta.sqlalchemy_session = db_session
    SuiteFactory._meta.sqlalchemy_session = db_session


register(SuiteResultFactory)
register(SuiteFactory)
