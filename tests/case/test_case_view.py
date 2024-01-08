import uuid

INVALID_USER_ID = uuid.uuid4()


def test_retrieve_case_by_id(client, case):
    response = client.get(url=f"/api/v1/cases/{case.id}")

    assert response.status_code == 200
    assert response.json()["id"] == case.id


def test_retrieve_case_by_invalid_id(client):
    response = client.get(url=f"/api/v1/cases/{INVALID_USER_ID}")

    assert response.status_code == 404


def test_create_case(client, case_factory):
    response = client.post(
        url="/api/v1/cases",
        json=case_factory.stub().__dict__,
    )

    assert response.status_code == 201


def test_update_case(client, case_factory, case):
    response = client.put(
        url=f"/api/v1/cases/{case.id}",
        json=case_factory.stub().__dict__,
    )

    assert response.status_code == 200
    assert response.json()["id"] == case.id


def test_update_case_by_invalid_id(client, case_factory):
    response = client.put(
        url=f"/api/v1/cases/{INVALID_USER_ID}",
        json=case_factory.stub().__dict__,
    )

    assert response.status_code == 404


def test_delete_case(client, case):
    response = client.delete(url=f"/api/v1/cases/{case.id}")

    assert response.status_code == 200


def test_delete_case_by_invalid_id(client):
    response = client.delete(url=f"/api/v1/cases/{INVALID_USER_ID}")

    assert response.status_code == 404
