import pytest
from fastapi.testclient import TestClient
from src.testgate.auth.crypto.password.library import PasswordHashLibrary
from src.testgate.auth.crypto.password.strategy import ScryptPasswordHashStrategy

password_hash_library = PasswordHashLibrary(ScryptPasswordHashStrategy())


@pytest.mark.parametrize("user__verified", [True])
@pytest.mark.parametrize(
    "user__password", [password_hash_library.encode("password_2024")]
)
async def test_login(client: TestClient, user_factory, user):
    response = client.post(
        url="/api/v1/auth/login",
        json=user_factory.stub(email=user.email, password="password_2024").__dict__,
    )
    assert response.status_code == 200
    assert response.json()["access_token"] is not None
    assert response.json()["refresh_token"] is not None


@pytest.mark.parametrize("user__verified", [True])
@pytest.mark.parametrize(
    "user__password", [password_hash_library.encode("password_2024")]
)
async def test_login_with_invalid_email(client: TestClient, user_factory, user):
    response = client.post(
        url="/api/v1/auth/login",
        json=user_factory.stub(
            email=f"invalid_{user.email}", password="password_2024"
        ).__dict__,
    )
    assert response.status_code == 404


@pytest.mark.parametrize(
    "user__password", [password_hash_library.encode("password_2024")]
)
async def test_login_with_invalid_verification(client: TestClient, user_factory, user):
    response = client.post(
        url="/api/v1/auth/login",
        json=user_factory.stub(email=user.email, password="password_2024").__dict__,
    )

    assert response.status_code == 403


@pytest.mark.parametrize("user__verified", [True])
@pytest.mark.parametrize(
    "user__password", [password_hash_library.encode("password_2024")]
)
async def test_login_with_invalid_password(client: TestClient, user_factory, user):
    response = client.post(
        url="/api/v1/auth/login",
        json=user_factory.stub(
            email=user.email, password="invalid_password_2024"
        ).__dict__,
    )

    assert response.status_code == 403


async def test_register(client: TestClient, user_factory):
    response = client.post(
        url="/api/v1/auth/register",
        json=user_factory.stub(password="password_2024").__dict__,
    )

    assert response.status_code == 200


async def test_register_with_existing_email(client: TestClient, user_factory, user):
    response = client.post(
        url="/api/v1/auth/register",
        json=user_factory.stub(email=user.email, password="password_2024").__dict__,
    )

    assert response.status_code == 409
