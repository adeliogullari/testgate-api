import pytest

from src.testgate.auth.oauth2.token.claims import Payload
from src.testgate.auth.oauth2.token.access import AccessToken
from src.testgate.auth.oauth2.token.refresh import RefreshToken


@pytest.fixture(scope="session")
def payload() -> Payload:
    return Payload()


@pytest.fixture(scope="session")
def access_token(request) -> AccessToken:
    return AccessToken(request.param)


@pytest.fixture(scope="session")
def refresh_token(request) -> RefreshToken:
    return RefreshToken(request.param)
