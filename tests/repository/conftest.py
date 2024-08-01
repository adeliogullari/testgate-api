from factory.faker import Faker
from src.testgate.repository.models import Repository
from factory.alchemy import SQLAlchemyModelFactory
from src.testgate.auth.crypto.password.library import PasswordHashLibrary

password_hash_library = PasswordHashLibrary(algorithm="scrypt")


class RepositoryFactory(SQLAlchemyModelFactory):
    class Meta:
        model = Repository
        sqlalchemy_session = None
        sqlalchemy_session_persistence = "flush"

    name = Faker("name")
