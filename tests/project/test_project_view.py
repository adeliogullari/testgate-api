import pytest


def test_retrieve_project_by_id(client, project):

    response = client.get(f"api/v1/project/{project.id}")

    assert response.status_code == 200


def test_retrieve_project_by_query_parameters(client, project):

    response = client.get(f"api/v1/projects", params={'name': project.name})

    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]['name'] == project.name


def test_create_role(client, make_role):

    response = client.post("api/v1/project", json=make_role())

    assert response.status_code == 201


def test_update_role(client, make_project, project):

    response = client.put(f"api/v1/project/{project.id}", json=make_project())

    assert response.status_code == 200


def test_delete_role(client, project):

    response = client.delete(f"api/v1/project/{project.id}")

    assert response.status_code == 200
