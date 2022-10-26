import pytest


def test_retrieve_run_by_id(client, run):

    response = client.get(f"api/v1/run/{run.id}")

    assert response.status_code == 200


def test_retrieve_run_by_query_parameters(client, run):

    response = client.get(f"api/v1/runs", params={'name': run.name})

    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]['name'] == run.name


def test_create_run(client, make_run):

    response = client.post("api/v1/run", json=make_run())

    assert response.status_code == 201


def test_update_run(client, make_run, run):

    response = client.put(f"api/v1/run/{run.id}", json=make_run())

    assert response.status_code == 200


def test_delete_run(client, run):

    response = client.delete(f"api/v1/run/{run.id}")

    assert response.status_code == 200
