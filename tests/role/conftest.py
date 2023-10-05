import pytest
from src.testgate.role.models import Role
from factory.alchemy import SQLAlchemyModelFactory
from pytest_factoryboy import register
from factory.faker import Faker
import factory


class RoleFactory(SQLAlchemyModelFactory):

    class Meta:
        model = Role
        sqlalchemy_session = None
        sqlalchemy_session_persistence = "flush"

    name = Faker('name')
    users = factory.RelatedFactoryList('tests.user.conftest.UserFactory', 'role', size=3)
    permissions = factory.RelatedFactoryList('tests.permission.conftest.PermissionFactory', 'roles', size=3)


@pytest.fixture(autouse=True)
def set_session_for_role_factory(db_session):
    RoleFactory._meta.sqlalchemy_session = db_session


register(RoleFactory)
