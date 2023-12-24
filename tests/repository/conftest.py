from factory.faker import Faker
from src.testgate.repository.models import Repository
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
