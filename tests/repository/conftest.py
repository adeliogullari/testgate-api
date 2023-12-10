import pytest
from factory.faker import Faker
from src.testgate.repository.models import Repository
from pytest_factoryboy import register
from factory.alchemy import SQLAlchemyModelFactory
from src.testgate.auth.crypto.password.library import PasswordHashLibrary
from src.testgate.auth.crypto.password.strategy import ScryptPasswordHashStrategy

password_hash_library = PasswordHashLibrary(ScryptPasswordHashStrategy())


class RepositoryFactory(SQLAlchemyModelFactory):
    class Meta:
        model = Repository
        sqlalchemy_session = None
        sqlalchemy_session_persistence = "flush"

    name = Faker("name")


@pytest.fixture(autouse=True)
def set_session_for_repository_factory(db_session):
    RepositoryFactory._meta.sqlalchemy_session = db_session


register(RepositoryFactory)
