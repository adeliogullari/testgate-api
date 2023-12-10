import pytest
from factory.faker import Faker
from src.testgate.permission.models import Permission
from pytest_factoryboy import register
from factory.alchemy import SQLAlchemyModelFactory


class PermissionFactory(SQLAlchemyModelFactory):
    class Meta:
        model = Permission
        sqlalchemy_session = None
        sqlalchemy_session_persistence = "flush"

    name = Faker("name")


@pytest.fixture(autouse=True)
def set_session_for_permission_factory(db_session):
    PermissionFactory._meta.sqlalchemy_session = db_session


register(PermissionFactory)
