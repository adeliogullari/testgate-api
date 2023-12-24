import pytest
import factory
from config import Settings
from factory.faker import Faker
from factory.alchemy import SQLAlchemyModelFactory
from tests.role.conftest import RoleFactory
from src.testgate.user.models import User
from src.testgate.auth.crypto.password.library import PasswordHashLibrary
from src.testgate.auth.crypto.password.strategy import ScryptPasswordHashStrategy
from datetime import datetime, timedelta
from src.testgate.auth.oauth2.token.access import AccessToken
from src.testgate.auth.crypto.digest.strategy import Blake2bMessageDigestStrategy

settings = Settings()
password_hash_library = PasswordHashLibrary(ScryptPasswordHashStrategy())


class UserFactory(SQLAlchemyModelFactory):
    class Meta:
        model = User
        sqlalchemy_session = None
        sqlalchemy_session_persistence = "flush"

    firstname = Faker("first_name")
    lastname = Faker("last_name")
    username = Faker("user_name")
    email = Faker("email")
    password = Faker("password")
    verified = False
    image = Faker("name")
    role = factory.SubFactory(RoleFactory)

    @factory.post_generation
    def role_generation(self, create, extracted, **kwargs):
        if not create:
            self.role = self.role.__dict__["name"]

    @factory.post_generation
    def password_generation(self, create, extracted, **kwargs):
        if create:
            self.password = password_hash_library.encode(str(self.password))


@pytest.fixture
def token(user):
    access_token = AccessToken(Blake2bMessageDigestStrategy())

    now = datetime.utcnow()
    exp = (now + timedelta(minutes=60)).timestamp()
    payload = {"exp": exp, "email": user.email}
    return access_token.encode(
        payload=payload,
        key=settings.testgate_jwt_access_token_key,
        headers={"alg": settings.testgate_jwt_access_token_alg, "typ": "JWT"},
    )


@pytest.fixture
def headers(token):
    return {"Authorization": f"Bearer {token}"}
