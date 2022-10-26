import pytest
from src.testgate.auth.schemas import AuthLoginRequestModel, AuthRegisterRequestModel


def test_login(client, user):

    response = client.post("api/v1/auth/login", json=AuthLoginRequestModel(**user.__dict__).json())

    assert response.status_code == 201


def test_register(client, user):

    response = client.post("api/v1/auth/register", json=AuthRegisterRequestModel(**user.__dict__).json())

    assert response.status_code == 201
