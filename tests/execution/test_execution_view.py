import random
from fastapi.testclient import TestClient
from src.testgate.execution.models import Execution
from tests.execution.conftest import ExecutionFactory

INVALID_EXECUTION_ID = random.randint(1, 1000)


async def test_create_execution(
    client: TestClient, execution_factory: ExecutionFactory
) -> None:
    response = client.post("api/v1/executions", json=execution_factory.stub().__dict__)

    assert response.status_code == 201


async def test_retrieve_execution_by_id(
    client: TestClient, execution: Execution
) -> None:
    response = client.get(f"api/v1/executions/{execution.id}")

    assert response.status_code == 200


async def test_retrieve_execution_by_invalid_id(
    client: TestClient, execution: Execution
) -> None:
    response = client.get(f"api/v1/executions/{INVALID_EXECUTION_ID}")

    assert response.status_code == 404


def test_retrieve_execution_by_query_parameters(
    client: TestClient, execution: Execution
) -> None:
    response = client.get(url="/api/v1/executions", params={"name": execution.name})

    assert response.status_code == 200
    assert response.json()[0]["id"] == execution.id


async def test_update_execution(
    client: TestClient, execution: Execution, execution_factory: ExecutionFactory
) -> None:
    response = client.put(
        f"api/v1/executions/{execution.id}", json=execution_factory.stub().__dict__
    )

    assert response.status_code == 200


def test_update_execution_by_invalid_id(
    client: TestClient, execution_factory: ExecutionFactory
) -> None:
    response = client.put(
        url=f"/api/v1/executions/{INVALID_EXECUTION_ID}",
        json=execution_factory.stub().__dict__,
    )

    assert response.status_code == 404


async def test_delete_execution(client: TestClient, execution: Execution) -> None:
    response = client.delete(f"api/v1/executions/{execution.id}")

    assert response.status_code == 200


def test_delete_execution_by_invalid_id(client: TestClient) -> None:
    response = client.delete(url=f"/api/v1/executions/{INVALID_EXECUTION_ID}")

    assert response.status_code == 404
