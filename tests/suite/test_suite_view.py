from fastapi.testclient import TestClient
from src.testgate.suite.models import Suite
from tests.suite.conftest import SuiteFactory


async def test_retrieve_suite_by_id(client: TestClient, suite: Suite) -> None:
    response = client.get(f"api/v1/suite/{suite.id}")

    assert response.status_code == 200


async def test_create_suite(client: TestClient, suite_factory: SuiteFactory) -> None:
    response = client.post("api/v1/suite", json=suite_factory.stub().__dict__)

    assert response.status_code == 201


async def test_update_suite(
    client: TestClient, suite_factory: SuiteFactory, suite: Suite
) -> None:
    response = client.put(
        f"api/v1/suite/{suite.id}", json=suite_factory.stub().__dict__
    )

    assert response.status_code == 200


async def test_delete_suite(client: TestClient, suite: Suite) -> None:
    response = client.delete(f"api/v1/suite/{suite.id}")

    assert response.status_code == 200
