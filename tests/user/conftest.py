import pytest
import factory
from typing import Any
from config import Settings
from factory.faker import Faker
from factory.alchemy import SQLAlchemyModelFactory
from tests.role.conftest import RoleFactory
from src.testgate.user.models import User
from src.testgate.auth.crypto.password.library import PasswordHashLibrary
from datetime import datetime, timedelta
from src.testgate.auth.oauth2.token.access import AccessToken
from starlette.datastructures import Headers

settings = Settings()
password_hash_library = PasswordHashLibrary(algorithm="scrypt")


class UserFactory(SQLAlchemyModelFactory):
    class Meta:
        model = User
        sqlalchemy_session = None
        sqlalchemy_session_persistence = "flush"

    firstname = Faker("first_name")
    lastname = Faker("last_name")
    username = Faker("user_name")
    email = Faker("email")
    password = Faker("binary")
    verified = False
    image = Faker("name")
    role = factory.SubFactory(RoleFactory)

    @factory.post_generation
    def role_generation(self, create: Any, extracted: Any, **kwargs: Any) -> None:
        if not create:
            self.role = self.role.__dict__["name"]


@pytest.fixture
def token(user: User) -> str:
    access_token = AccessToken("blake2b")

    now = datetime.utcnow()
    exp = (now + timedelta(minutes=60)).timestamp()
    payload = {"exp": exp, "email": user.email}
    return access_token.encode(
        payload=payload,
        key=settings.testgate_jwt_access_token_key,
        headers={"alg": settings.testgate_jwt_access_token_algorithm, "typ": "JWT"},
    )


@pytest.fixture
def headers(token: str) -> Headers:
    return Headers({"Authorization": f"Bearer {token}"})
