import pytest
from factory.faker import Faker
from factory.alchemy import SQLAlchemyModelFactory
from src.testgate.role.models import Role
from pytest_factoryboy import register


class RoleFactory(SQLAlchemyModelFactory):
    class Meta:
        model = Role
        sqlalchemy_session = None
        sqlalchemy_session_persistence = "flush"

    name = Faker("name")


@pytest.fixture(autouse=True)
def set_session_for_role_factory(db_session):
    RoleFactory._meta.sqlalchemy_session = db_session


register(RoleFactory)
