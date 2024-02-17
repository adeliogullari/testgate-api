from factory.faker import Faker
from src.testgate.permission.models import Permission
from factory.alchemy import SQLAlchemyModelFactory


class PermissionFactory(SQLAlchemyModelFactory):
    class Meta:
        model = Permission
        sqlalchemy_session = None
        sqlalchemy_session_persistence = "flush"

    name = Faker("name")
