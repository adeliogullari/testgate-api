import pytest

from src.testgate.auth.crypto.password.pbkdf2 import Pbkdf2
from src.testgate.auth.crypto.password.scrypt import Scrypt


@pytest.fixture(scope="session")
def pbkdf2() -> Pbkdf2:
    return Pbkdf2()


@pytest.fixture(scope='session')
def scrypt() -> Scrypt:
    return Scrypt()
