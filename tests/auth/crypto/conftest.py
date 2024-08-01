import pytest
from pytest import FixtureRequest
from src.testgate.auth.crypto.digest.library import MessageDigestLibrary
from src.testgate.auth.crypto.digest.blake2b import Blake2b
from src.testgate.auth.crypto.password.pbkdf2 import Pbkdf2
from src.testgate.auth.crypto.password.scrypt import Scrypt
from src.testgate.auth.crypto.password.library import PasswordHashLibrary


@pytest.fixture(scope="session")
def blake2b() -> Blake2b:
    return Blake2b()


@pytest.fixture(scope="session")
def message_digest_library(request: FixtureRequest) -> MessageDigestLibrary:
    return MessageDigestLibrary(request.param)


@pytest.fixture(scope="session")
def pbkdf2() -> Pbkdf2:
    return Pbkdf2()


@pytest.fixture(scope="session")
def scrypt() -> Scrypt:
    return Scrypt()


@pytest.fixture(scope="session")
def password_hash_library(request: FixtureRequest) -> PasswordHashLibrary:
    return PasswordHashLibrary(request.param)
