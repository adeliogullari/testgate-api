import uuid
import random
import pytest
from starlette.datastructures import Headers
from fastapi.testclient import TestClient
from src.testgate.user.models import User
from tests.user.conftest import UserFactory
from src.testgate.auth.crypto.password.library import PasswordHashLibrary

INVALID_ACCESS_TOKEN = uuid.uuid4()
INVALID_USER_ID = random.randint(1, 1000)

invalid_headers = {"Authorization": f"Bearer {INVALID_ACCESS_TOKEN}"}

password_hash_library = PasswordHashLibrary("scrypt")


async def test_retrieve_current_user(
    client: TestClient, user: User, headers: Headers
) -> None:
    response = client.get(url="/api/v1/me", headers=headers)

    assert response.status_code == 200
    assert response.json()["id"] == user.id


async def test_retrieve_current_user_with_invalid_token(client: TestClient) -> None:
    response = client.get(url="/api/v1/me", headers=invalid_headers)

    assert response.status_code == 403


async def test_retrieve_user_by_id(
    client: TestClient, user: User, headers: Headers
) -> None:
    response = client.get(url=f"/api/v1/users/{user.id}", headers=headers)

    assert response.status_code == 200
    assert response.json()["id"] == user.id


async def test_retrieve_user_by_invalid_id(client: TestClient, headers: dict) -> None:
    response = client.get(url=f"/api/v1/users/{INVALID_USER_ID}", headers=headers)

    assert response.status_code == 404


async def test_create_user(
    client: TestClient, user_factory: UserFactory, headers: Headers
) -> None:
    response = client.post(
        url="/api/v1/users",
        json=user_factory.stub(password="password_2024").__dict__,
        headers=headers,
    )

    assert response.status_code == 201


async def test_create_user_with_existing_username(
    client: TestClient, user_factory: UserFactory, user: User, headers: Headers
) -> None:
    response = client.post(
        url="/api/v1/users",
        json=user_factory.stub(
            username=user.username, password="password_2024"
        ).__dict__,
        headers=headers,
    )

    assert response.status_code == 409


async def test_create_user_with_existing_email(
    client: TestClient, user_factory: UserFactory, user: User, headers: Headers
) -> None:
    response = client.post(
        url="/api/v1/users",
        json=user_factory.stub(email=user.email, password="password_2024").__dict__,
        headers=headers,
    )

    assert response.status_code == 409


async def test_update_current_user(
    client: TestClient, user_factory: UserFactory, user: User, headers: Headers
) -> None:
    response = client.put(
        url="/api/v1/me",
        json=user_factory.stub(password="password_2024").__dict__,
        headers=headers,
    )

    assert response.status_code == 200
    assert response.json()["id"] == user.id


async def test_update_current_user_with_invalid_token(
    client: TestClient, user_factory: UserFactory
) -> None:
    response = client.put(
        url="/api/v1/me",
        json=user_factory.stub(password="password_2024").__dict__,
        headers=invalid_headers,
    )

    assert response.status_code == 403


async def test_update_user(
    client: TestClient, user_factory: UserFactory, user: User, headers: Headers
) -> None:
    response = client.put(
        url=f"/api/v1/users/{user.id}",
        json=user_factory.stub(password="password_2024").__dict__,
        headers=headers,
    )

    assert response.status_code == 200
    assert response.json()["id"] == user.id


async def test_update_user_by_invalid_id(
    client: TestClient, user_factory: UserFactory, headers: Headers
) -> None:
    response = client.put(
        url=f"/api/v1/users/{INVALID_USER_ID}",
        json=user_factory.stub(password="password_2024").__dict__,
        headers=headers,
    )

    assert response.status_code == 404


async def test_verify_current_user(client: TestClient, token: str) -> None:
    response = client.get(url=f"/api/v1/users/email/verify/{token}")

    assert response.status_code == 200
    assert response.json()["verified"] is True


async def test_verify_current_user_with_invalid_token(client: TestClient) -> None:
    response = client.get(url=f"/api/v1/users/email/verify/{INVALID_ACCESS_TOKEN}")

    assert response.status_code == 403


@pytest.mark.parametrize(
    "user__password", [password_hash_library.encode("password_2024")]
)
async def test_update_current_user_password(
    client: TestClient, user: User, headers: Headers
) -> None:
    response = client.put(
        url="/api/v1/me/change-password",
        json={
            "current_password": "password_2024",
            "password": "new_password_2024",
            "password_confirmation": "new_password_2024",
        },
        headers=headers,
    )

    assert response.status_code == 201
    assert response.json()["id"] == user.id


async def test_update_current_user_password_with_invalid_token(
    client: TestClient,
) -> None:
    response = client.put(
        url="/api/v1/me/change-password",
        json={
            "current_password": "password_2024",
            "password": "new_password_2024",
            "password_confirmation": "new_password_2024",
        },
        headers=invalid_headers,
    )

    assert response.status_code == 403


async def test_delete_current_user(
    client: TestClient, user: User, headers: Headers
) -> None:
    response = client.delete(url="/api/v1/me", headers=headers)

    assert response.status_code == 200
    assert response.json()["id"] == user.id


async def test_delete_current_user_with_invalid_token(client: TestClient) -> None:
    response = client.delete(url="/api/v1/me", headers=invalid_headers)

    assert response.status_code == 403


async def test_delete_user(client: TestClient, user: User, headers: Headers) -> None:
    response = client.delete(url=f"/api/v1/users/{user.id}", headers=headers)

    assert response.status_code == 200


async def test_delete_user_by_invalid_id(client: TestClient, headers: Headers) -> None:
    response = client.delete(url=f"/api/v1/users/{INVALID_USER_ID}", headers=headers)

    assert response.status_code == 404
