import pytest
from pytest import FixtureRequest
from src.testgate.auth.oauth2.token.claims import Payload
from src.testgate.auth.oauth2.token.access import AccessToken
from src.testgate.auth.oauth2.token.refresh import RefreshToken


@pytest.fixture(scope="function")
def payload() -> Payload:
    return Payload()


@pytest.fixture(scope="function")
def access_token(request: FixtureRequest) -> AccessToken:
    return AccessToken(request.param)


@pytest.fixture(scope="function")
def refresh_token(request: FixtureRequest) -> RefreshToken:
    return RefreshToken(request.param)
