import pytest

from src.testgate.auth.crypto import (Blake2b,
                                      MessageDigestLibrary,
                                      Pbkdf2,
                                      Scrypt,
                                      PasswordHashLibrary)


@pytest.fixture(scope='session')
def blake2b() -> Blake2b:
    return Blake2b()


@pytest.fixture(scope='session')
def message_digest_library(request) -> MessageDigestLibrary:
    return MessageDigestLibrary(request.param)


@pytest.fixture(scope='session')
def pbkdf2() -> Pbkdf2:
    return Pbkdf2()


@pytest.fixture(scope='session')
def scrypt() -> Scrypt:
    return Scrypt()


@pytest.fixture(scope='session')
def password_hash_library(request) -> PasswordHashLibrary:
    return PasswordHashLibrary(request.param)
