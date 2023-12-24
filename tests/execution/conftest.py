import pytest
import factory
from factory.faker import Faker
from src.testgate.execution.models import Execution, ExecutionResult
from pytest_factoryboy import register
from factory.alchemy import SQLAlchemyModelFactory
from src.testgate.auth.crypto.password.library import PasswordHashLibrary
from src.testgate.auth.crypto.password.strategy import ScryptPasswordHashStrategy

password_hash_library = PasswordHashLibrary(ScryptPasswordHashStrategy())


class ExecutionResultFactory(SQLAlchemyModelFactory):
    class Meta:
        model = ExecutionResult
        sqlalchemy_session = None
        sqlalchemy_session_persistence = "flush"

    total = 0
    passed = 0
    failed = 0
    skipped = 0


class ExecutionFactory(SQLAlchemyModelFactory):
    class Meta:
        model = Execution
        sqlalchemy_session = None
        sqlalchemy_session_persistence = "flush"

    name = Faker("name")
    result = factory.SubFactory(ExecutionResultFactory)

    @factory.post_generation
    def result_generation(self, create, extracted, **kwargs):
        if not create:
            self.result = self.result.__dict__


@pytest.fixture(autouse=True)
def set_session_for_execution_factory(db_session):
    ExecutionResultFactory._meta.sqlalchemy_session = db_session
    ExecutionFactory._meta.sqlalchemy_session = db_session


register(ExecutionResultFactory)
register(ExecutionFactory)