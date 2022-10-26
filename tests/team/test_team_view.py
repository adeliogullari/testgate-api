import pytest
from src.testgate.user.schemas import UpdateUserRequestModel, UpdateUserResponseModel


def test_create_team(client, team_factory):

    response = client.post("api/v1/team", json=team_factory.stub().__dict__)

    assert response.status_code == 201


def test_retrieve_team_by_id(client, team):

    response = client.get(f"api/v1/team/{team.id}")

    assert response.status_code == 200


def test_retrieve_team_by_query_parameters(client, team):

    response = client.get(f"api/v1/teams", params={'name': team.name})

    assert response.status_code == 200


def test_update_team(client, team, team_factory):

    response = client.put(f"api/v1/team/{team.id}", json=team_factory.stub().__dict__)

    assert response.status_code == 200


def test_delete_team(client, team):

    response = client.delete(f"api/v1/team/{team.id}")

    assert response.status_code == 200
