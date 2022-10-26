import pytest
from src.testgate.run.models import Run
from factory.alchemy import SQLAlchemyModelFactory
from pytest_factoryboy import register


class RunFactory(SQLAlchemyModelFactory):

    class Meta:
        model = Run
        sqlalchemy_session = None
        sqlalchemy_session_persistence = "flush"

    name = "MyRun"
    result = None


@pytest.fixture(autouse=True)
def set_session_for_run_factory(db_session):
    RunFactory._meta.sqlalchemy_session = db_session


register(RunFactory)
