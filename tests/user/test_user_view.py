import pytest
from datetime import datetime, timedelta


@pytest.fixture
def token(user):
    from src.testgate.auth.oauth2 import AccessToken, RefreshToken
    from src.testgate.auth.crypto.digest.strategy import Blake2bMessageDigestStrategy

    access_token = AccessToken(Blake2bMessageDigestStrategy())
    refresh_token = RefreshToken(Blake2bMessageDigestStrategy())

    now = datetime.utcnow()
    exp = (now + timedelta(minutes=60)).timestamp()
    payload = {'exp': exp, 'email': user.email}
    return access_token.encode(payload=payload, key='key', headers={})


def test_create_user(client, user_factory):

    response = client.post("api/v1/users", json=user_factory.stub().__dict__)

    assert response.status_code == 201


def test_create_user_with_existing_email(client, user_factory, user):

    response = client.post("api/v1/users", json=user_factory.stub(email=user.email, password="147258DsA").__dict__)

    assert response.status_code == 409


def test_retrieve_current_user(client, user, token):

    response = client.get(f"api/v1/me", headers={"Authorization": f"bearer {token}"})

    assert response.status_code == 200


def test_retrieve_user_by_id(client, user):

    response = client.get(f"api/v1/users/{user.id}")

    assert response.status_code == 200


def test_verify_current_user(client, user, token):
    response = client.get(f"/api/v1/user/email/verify/{token}")

    assert response.status_code == 200
    assert response.json()['verified'] is True


@pytest.mark.parametrize("user__password", ["password_2024"])
def test_change_current_user_password(client, token):
    response = client.put(f"api/v1/me/change-password",
                          json={'current_password': "password_2024",
                                'password': 'new_password_2024',
                                'password_confirmation': 'new_password_2024'},
                          headers={"Authorization": f"bearer {token}"})

    assert response.status_code == 201


def test_delete_current_user_by_token(client, token):

    response = client.delete(f"api/v1/user/me", headers={"Authorization": f"bearer {token}"})

    assert response.status_code == 200


def test_delete_user_by_id(client, user, token):

    response = client.delete(f"api/v1/user/{user.id}", headers={"Authorization": f"bearer {token}"})

    assert response.status_code == 200
