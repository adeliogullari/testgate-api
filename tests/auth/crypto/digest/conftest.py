import pytest

from src.testgate.auth.crypto.digest import Blake2b


@pytest.fixture(scope='session')
def blake2b() -> Blake2b:
    return Blake2b()
