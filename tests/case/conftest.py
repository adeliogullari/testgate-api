import factory
from typing import Any
from factory.alchemy import SQLAlchemyModelFactory
from src.testgate.case.models import Case, CaseResult


class CaseResultFactory(SQLAlchemyModelFactory):
    class Meta:
        model = CaseResult
        sqlalchemy_session = None
        sqlalchemy_session_persistence = "flush"

    total = 0
    passed = 0
    failed = 0
    skipped = 0


class CaseFactory(SQLAlchemyModelFactory):
    class Meta:
        model = Case
        sqlalchemy_session = None
        sqlalchemy_session_persistence = "flush"

    name = "MyCase"
    description = "Description"
    result = factory.SubFactory(CaseResultFactory)

    @factory.post_generation
    def result_generation(self, create: Any, extracted: Any, **kwargs: Any) -> None:
        if not create:
            self.result = self.result.__dict__
