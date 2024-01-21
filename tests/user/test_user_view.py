import uuid
import random
import pytest
from src.testgate.auth.crypto.password.library import PasswordHashLibrary
from src.testgate.auth.crypto.password.strategy import ScryptPasswordHashStrategy

INVALID_ACCESS_TOKEN = uuid.uuid4()
INVALID_USER_ID = random.randint(1, 1000)

invalid_headers = {"Authorization": f"bearer {INVALID_ACCESS_TOKEN}"}

password_pash_library = PasswordHashLibrary(ScryptPasswordHashStrategy())


def test_retrieve_current_user(client, user, headers):
    response = client.get(url="/api/v1/me", headers=headers)

    assert response.status_code == 200
    assert response.json()["id"] == user.id


def test_retrieve_current_user_with_invalid_token(client):
    response = client.get(url="/api/v1/me", headers=invalid_headers)

    assert response.status_code == 403


@pytest.mark.parametrize("role__name", ["Admin"])
def test_retrieve_user_by_id(client, user, headers):
    response = client.get(url=f"/api/v1/users/{user.id}", headers=headers)

    assert response.status_code == 200
    assert response.json()["id"] == user.id


@pytest.mark.parametrize("role__name", ["Admin"])
def test_retrieve_user_by_invalid_id(client, headers):
    response = client.get(url=f"/api/v1/users/{INVALID_USER_ID}", headers=headers)

    assert response.status_code == 404


def test_create_user(client, user_factory, headers):
    response = client.post(
        url="/api/v1/users", json=user_factory.stub(password="password_2024").__dict__, headers=headers
    )

    assert response.status_code == 201


def test_create_user_with_existing_username(client, user_factory, user, headers):
    response = client.post(
        url="/api/v1/users",
        json=user_factory.stub(username=user.username, password="password_2024").__dict__,
        headers=headers,
    )

    assert response.status_code == 409


def test_create_user_with_existing_email(client, user_factory, user, headers):
    response = client.post(
        url="/api/v1/users",
        json=user_factory.stub(email=user.email, password="password_2024").__dict__,
        headers=headers,
    )

    assert response.status_code == 409


def test_update_current_user(client, user_factory, user, headers):
    response = client.put(
        url="/api/v1/me", json=user_factory.stub(password="password_2024").__dict__, headers=headers
    )

    assert response.status_code == 200
    assert response.json()["id"] == user.id


def test_update_current_user_with_invalid_token(client, user_factory):
    response = client.put(
        url="/api/v1/me", json=user_factory.stub(password="password_2024").__dict__, headers=invalid_headers
    )

    assert response.status_code == 403


def test_update_user(client, user_factory, user, headers):
    response = client.put(
        url=f"/api/v1/users/{user.id}",
        json=user_factory.stub(password="password_2024").__dict__,
        headers=headers,
    )

    assert response.status_code == 200
    assert response.json()["id"] == user.id


def test_update_user_by_invalid_id(client, user_factory, headers):
    response = client.put(
        url=f"/api/v1/users/{INVALID_USER_ID}",
        json=user_factory.stub(password="password_2024").__dict__,
        headers=headers,
    )

    assert response.status_code == 404


def test_verify_current_user(client, token):
    response = client.get(url=f"/api/v1/users/email/verify/{token}")

    assert response.status_code == 200
    assert response.json()["verified"] is True


def test_verify_current_user_with_invalid_token(client):
    response = client.get(url=f"/api/v1/users/email/verify/{INVALID_ACCESS_TOKEN}")

    assert response.status_code == 403


@pytest.mark.parametrize("user__password", [password_pash_library.encode("password_2024")])
def test_update_current_user_password(client, user, headers):
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


def test_update_current_user_password_with_invalid_token(client):
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


def test_delete_current_user(client, user, headers):
    response = client.delete(url="/api/v1/me", headers=headers)

    assert response.status_code == 200
    assert response.json()["id"] == user.id


def test_delete_current_user_with_invalid_token(client):
    response = client.delete(url="/api/v1/me", headers=invalid_headers)

    assert response.status_code == 403


def test_delete_user(client, user, headers):
    response = client.delete(url=f"/api/v1/users/{user.id}", headers=headers)

    assert response.status_code == 200


def test_delete_user_by_invalid_id(client, headers):
    response = client.delete(url=f"/api/v1/users/{INVALID_USER_ID}", headers=headers)

    assert response.status_code == 404
