import pytest
import factory
from factory import SubFactory
from factory.faker import Faker
from src.testgate.user.models import User
from pytest_factoryboy import register
from factory.alchemy import SQLAlchemyModelFactory
from tests.role.conftest import RoleFactory
from tests.team.conftest import TeamFactory
from src.testgate.auth.crypto.password.library import PasswordHashLibrary
from src.testgate.auth.crypto.password.strategy import ScryptPasswordHashStrategy

password_hash_library = PasswordHashLibrary(ScryptPasswordHashStrategy())


class UserFactory(SQLAlchemyModelFactory):

    class Meta:
        model = User
        sqlalchemy_session = None
        sqlalchemy_session_persistence = "flush"

    firstname = Faker('first_name')
    lastname = Faker('last_name')
    username = Faker('user_name')
    email = Faker('email')
    password = Faker('password')
    verified = False
    image = Faker('name')
    role = SubFactory(RoleFactory)
    team = SubFactory(TeamFactory)

    @factory.post_generation
    def role_generation(self, create, extracted, **kwargs):
        if not create:
            self.role = self.role.__dict__['name']

    @factory.post_generation
    def team_generation(self, create, extracted, **kwargs):
        if not create:
            self.team = self.team.__dict__['name']

    @factory.post_generation
    def password_generation(self, create, extracted, **kwargs):
        if create:
            self.password = password_hash_library.encode(str(self.password))


@pytest.fixture(autouse=True)
def set_session_for_user_factory(db_session):
    UserFactory._meta.sqlalchemy_session = db_session


register(UserFactory)
