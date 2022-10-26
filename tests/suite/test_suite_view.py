import pytest


def test_retrieve_suite_by_id(client, suite):

    response = client.get(f"api/v1/suite/{suite.id}")

    assert response.status_code == 200


def test_create_suite(client, make_suite):

    response = client.post("api/v1/suite", json=make_suite())

    assert response.status_code == 201


def test_update_suite(client, make_suite, suite):

    response = client.put(f"api/v1/suite/{suite.id}", json=make_suite())

    assert response.status_code == 200


def test_delete_suite(client, suite):

    response = client.delete(f"api/v1/suite/{suite.id}")

    assert response.status_code == 200
