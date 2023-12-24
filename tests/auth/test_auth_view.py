import pytest


@pytest.mark.parametrize("user__password", ["password_2024"])
def test_login_with_valid_credentials(client, user_factory, user):
    response = client.post(
        url="/api/v1/auth/login",
        json=user_factory.stub(email=user.email, password="password_2024").__dict__,
    )

    assert response.status_code == 200
    assert response.json()["access_token"] is not None
    assert response.json()["refresh_token"] is not None


@pytest.mark.parametrize("user__email", ["email_2024@gmail.com"])
@pytest.mark.parametrize("user__password", ["password_2024"])
def test_login_with_invalid_email(client, user_factory, user):
    response = client.post(
        url="/api/v1/auth/login",
        json=user_factory.stub(
            email="invalid_email_2024@gmail.com", password="password_2024"
        ).__dict__,
    )
    assert response.status_code == 404


@pytest.mark.parametrize("user__password", ["password_2023"])
def test_login_with_invalid_password(client, user_factory, user):
    response = client.post(
        url="/api/v1/auth/login",
        json=user_factory.stub(
            email=user.email, password="invalid_password_2024"
        ).__dict__,
    )

    assert response.status_code == 403


def test_register_with_valid_credentials(client, user_factory):
    response = client.post("/api/v1/auth/register", json=user_factory.stub().__dict__)

    assert response.status_code == 201


def test_register_with_existing_email(client, user_factory, user):
    response = client.post(
        "/api/v1/auth/register", json=user_factory.stub(email=user.email).__dict__
    )

    assert response.status_code == 409
