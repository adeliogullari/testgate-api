import pytest


def test_create_user(client, user_factory):

    response = client.post("api/v1/users", json=user_factory.stub().__dict__)

    assert response.status_code == 201


def test_create_user_with_existing_email(client, user_factory, user):

    response = client.post("api/v1/users", json=user_factory.stub(email=user.email, password="147258DsA").__dict__)

    assert response.status_code == 409


def test_retrieve_current_user(client, user, auth):

    response = client.get(f"api/v1/me", headers={"Authorization": f"bearer {auth}"})

    assert response.status_code == 200


def test_retrieve_user_by_id(client, user):

    response = client.get(f"api/v1/users/{user.id}")

    assert response.status_code == 200


def test_verify_current_user(client, user, auth):
    response = client.get(f"/api/v1/user/email/verify/{auth}")

    assert response.status_code == 200
    assert response.json()['verified'] is True


def test_change_current_user_password(client, user, auth):
    current_password: str
    password: str
    password_confirmation: str
    response = client.put(f"/api/v1/me/change-password", json={'current_password': None,
                                                               'password': '19941995klm',
                                                               'password_confirmation': '19941995klm'}, headers={"Authorization": f"bearer {auth}"})

    assert response.status_code == 201


def test_authenticate_user(client, user):

    response = client.post(f"api/v1/user/auth", json={'email': user.email, 'password': '147258DsA&'})

    assert response.status_code == 200


def test_delete_current_user_by_token(client, auth):

    response = client.delete(f"api/v1/user/me", headers={"Authorization": f"bearer {auth}"})

    assert response.status_code == 200


def test_delete_user(client, user, auth):

    response = client.delete(f"api/v1/user/{user.id}", headers={"Authorization": f"bearer {auth}"})

    assert response.status_code == 200
