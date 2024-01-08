from factory.faker import Faker
from factory.alchemy import SQLAlchemyModelFactory
from src.testgate.role.models import Role


class RoleFactory(SQLAlchemyModelFactory):
    class Meta:
        model = Role
        sqlalchemy_session = None
        sqlalchemy_session_persistence = "flush"

    name = Faker("name")
