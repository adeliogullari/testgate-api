import random
from fastapi.testclient import TestClient
from src.testgate.case.models import Case
from tests.case.conftest import CaseFactory

INVALID_USER_ID = random.randint(1, 1000)


def test_retrieve_case_by_id(client: TestClient, case: Case):
    response = client.get(url=f"/api/v1/cases/{case.id}")

    assert response.status_code == 200
    assert response.json()["id"] == case.id


def test_retrieve_case_by_invalid_id(client: TestClient):
    response = client.get(url=f"/api/v1/cases/{INVALID_USER_ID}")

    assert response.status_code == 404


def test_retrieve_case_by_query_parameters(client: TestClient, case: Case):
    response = client.get(url=f"/api/v1/cases", params={"name": case.name})

    assert response.status_code == 200
    assert response.json()[0]["id"] == case.id


def test_create_case(client: TestClient, case_factory: CaseFactory):
    response = client.post(
        url="/api/v1/cases",
        json=case_factory.stub().__dict__,
    )

    assert response.status_code == 201
    assert response.json()["name"] == case_factory.name


def test_update_case(client: TestClient, case_factory: CaseFactory, case: Case):
    response = client.put(
        url=f"/api/v1/cases/{case.id}",
        json=case_factory.stub().__dict__,
    )

    assert response.status_code == 200
    assert response.json()["id"] == case.id


def test_update_case_by_invalid_id(client: TestClient, case_factory: CaseFactory):
    response = client.put(
        url=f"/api/v1/cases/{INVALID_USER_ID}",
        json=case_factory.stub().__dict__,
    )

    assert response.status_code == 404


def test_delete_case(client: TestClient, case: Case):
    response = client.delete(url=f"/api/v1/cases/{case.id}")

    assert response.status_code == 200
    assert response.json()["id"] == case.id


def test_delete_case_by_invalid_id(client: TestClient):
    response = client.delete(url=f"/api/v1/cases/{INVALID_USER_ID}")

    assert response.status_code == 404
