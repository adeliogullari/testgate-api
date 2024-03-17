from fastapi.testclient import TestClient


async def test_create_execution(client: TestClient, execution_factory):
    response = client.post("api/v1/executions", json=execution_factory.stub().__dict__)

    assert response.status_code == 201


async def test_create_execution_with_existing_name(
    client: TestClient, execution_factory, execution
):
    response = client.post(
        "api/v1/executions", json=execution_factory.stub(name=execution.name).__dict__
    )

    assert response.status_code == 409


async def test_retrieve_execution_by_id(client: TestClient, execution):
    response = client.get(f"api/v1/executions/{execution.id}")

    assert response.status_code == 200


async def test_update_execution(client: TestClient, execution, execution_factory):
    response = client.put(
        f"api/v1/executions/{execution.id}", json=execution_factory.stub().__dict__
    )

    assert response.status_code == 200


async def test_delete_execution(client: TestClient, execution):
    response = client.delete(f"api/v1/executions/{execution.id}")

    assert response.status_code == 200
