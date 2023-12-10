import pytest


@pytest.mark.parametrize("role__name", ["Admin"])
def test_create_user(client, user_factory, role, token):
    response = client.post(
        url="api/v1/users",
        json=user_factory.stub(role=role).__dict__,
        headers={"Authorization": f"bearer {token}"},
    )

    assert response.status_code == 201


def test_create_user_with_invalid_token(client, user_factory):
    response = client.post(
        "api/v1/users",
        json=user_factory.stub().__dict__,
        headers={"Authorization": "bearer InvalidToken"},
    )

    assert response.status_code == 403


@pytest.mark.parametrize("role__name", ["Admin"])
def test_create_user_with_existing_email(client, user_factory, user, role, token):
    response = client.post(
        "api/v1/users",
        json=user_factory.stub(email=user.email, role=role).__dict__,
        headers={"Authorization": f"bearer {token}"},
    )

    assert response.status_code == 409


def test_retrieve_current_user(client, user, token):
    response = client.get("api/v1/me", headers={"Authorization": f"bearer {token}"})

    assert response.status_code == 200


def test_retrieve_current_user_with_invalid_token(client, user, token):
    response = client.get("api/v1/me", headers={"Authorization": "bearer InvalidToken"})

    assert response.status_code == 403


@pytest.mark.parametrize("role__name", ["Admin"])
def test_retrieve_user_by_id(client, user, token):
    response = client.get(
        f"api/v1/users/{user.id}", headers={"Authorization": f"bearer {token}"}
    )

    assert response.status_code == 200


def test_retrieve_user_by_id_with_invalid_token(client, user, token):
    response = client.get(
        f"api/v1/users/{user.id}", headers={"Authorization": "bearer InvalidToken"}
    )

    assert response.status_code == 403


@pytest.mark.parametrize("role__name", ["Admin"])
def test_verify_current_user(client, user, token):
    response = client.get(
        f"/api/v1/user/email/verify/{token}",
        headers={"Authorization": f"bearer {token}"},
    )

    assert response.status_code == 200
    assert response.json()["verified"] is True


@pytest.mark.parametrize("user__password", ["password_2024"])
def test_change_current_user_password(client, token):
    response = client.put(
        "api/v1/me/change-password",
        json={
            "current_password": "password_2024",
            "password": "new_password_2024",
            "password_confirmation": "new_password_2024",
        },
        headers={"Authorization": f"bearer {token}"},
    )

    assert response.status_code == 201


@pytest.mark.parametrize("role__name", ["Admin"])
def test_delete_current_user(client, user, token):
    response = client.delete(
        "api/v1/user/me", headers={"Authorization": f"bearer {token}"}
    )

    assert response.status_code == 200


@pytest.mark.parametrize("role__name", ["Admin"])
def test_delete_user_by_id(client, user, token):
    response = client.delete(
        f"api/v1/user/{user.id}", headers={"Authorization": f"bearer {token}"}
    )

    assert response.status_code == 200
