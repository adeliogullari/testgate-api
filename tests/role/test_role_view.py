import pytest


def test_retrieve_role_by_id(client, role):

    response = client.get(f"api/v1/role/{role.id}")

    assert response.status_code == 200


def test_search_role(client, role):

    response = client.get(f"api/v1/roles", params={'name': role.name})

    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]['name'] == role.name


def test_create_role(client, role_factory):

    response = client.post("api/v1/role", json=role_factory.stub().__dict__)

    assert response.status_code == 201


def test_update_role(client, role, role_factory):

    response = client.put(f"api/v1/role/{role.id}", json=role_factory.stub().__dict__)

    assert response.status_code == 200


def test_delete_role(client, role):

    response = client.delete(f"api/v1/role/{role.id}")

    assert response.status_code == 200
