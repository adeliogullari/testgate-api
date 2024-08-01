import factory
from typing import Any
from factory.faker import Faker
from src.testgate.execution.models import (
    Execution,
    ExecutionJob,
    ExecutionRunner,
    ExecutionResult,
)
from factory.alchemy import SQLAlchemyModelFactory
from src.testgate.auth.crypto.password.library import PasswordHashLibrary

password_hash_library = PasswordHashLibrary(algorithm="scrypt")


class ExecutionJobFactory(SQLAlchemyModelFactory):
    class Meta:
        model = ExecutionJob
        sqlalchemy_session = None
        sqlalchemy_session_persistence = "flush"

    id = 1
    name = Faker("name")


class ExecutionRunnerFactory(SQLAlchemyModelFactory):
    class Meta:
        model = ExecutionRunner
        sqlalchemy_session = None
        sqlalchemy_session_persistence = "flush"

    id = 1
    name = Faker("name")


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
    runner = factory.SubFactory(ExecutionRunnerFactory)

    @factory.post_generation
    def result_generation(self, create: Any, extracted: Any, **kwargs: Any) -> None:
        if not create:
            self.result = self.result.__dict__

    @factory.post_generation
    def runner_generation(self, create: Any, extracted: Any, **kwargs: Any) -> None:
        if not create:
            self.runner = self.runner.__dict__
