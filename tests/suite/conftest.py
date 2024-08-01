from typing import Any
import factory
from src.testgate.suite.models import Suite, SuiteResult
from factory.alchemy import SQLAlchemyModelFactory


class SuiteResultFactory(SQLAlchemyModelFactory):
    class Meta:
        model = SuiteResult
        sqlalchemy_session = None
        sqlalchemy_session_persistence = "flush"

    id = 1
    total = 0
    passed = 0
    failed = 0
    skipped = 0


class SuiteFactory(SQLAlchemyModelFactory):
    class Meta:
        model = Suite
        sqlalchemy_session = None
        sqlalchemy_session_persistence = "flush"

    id = 1
    name = "MySuite"
    description = "Description"
    result = factory.SubFactory(SuiteResultFactory)

    @factory.post_generation
    def result_generation(self, create: Any, extracted: Any, **kwargs: Any) -> None:
        if not create:
            self.result = self.result.__dict__
