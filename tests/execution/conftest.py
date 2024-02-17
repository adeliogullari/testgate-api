import factory
from factory.faker import Faker
from src.testgate.execution.models import Execution, ExecutionResult
from factory.alchemy import SQLAlchemyModelFactory
from src.testgate.auth.crypto.password.library import PasswordHashLibrary
from src.testgate.auth.crypto.password.strategy import ScryptPasswordHashStrategy

password_hash_library = PasswordHashLibrary(ScryptPasswordHashStrategy())


class ExecutionResultFactory(SQLAlchemyModelFactory):
    class Meta:
        model = ExecutionResult
        sqlalchemy_session = None
        sqlalchemy_session_persistence = "flush"

    id = 1
    total = 15
    passed = 5
    failed = 5
    skipped = 5


class ExecutionFactory(SQLAlchemyModelFactory):
    class Meta:
        model = Execution
        sqlalchemy_session = None
        sqlalchemy_session_persistence = "flush"

    id = 1
    name = Faker("name")
    result = factory.SubFactory(ExecutionResultFactory)

    @factory.post_generation
    def result_generation(self, create, extracted, **kwargs):
        if not create:
            self.result = self.result.__dict__
