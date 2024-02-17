def test_create_execution(client, execution_factory):
    response = client.post("api/v1/executions", json=execution_factory.stub().__dict__)

    assert response.status_code == 201


def test_create_execution_with_existing_name(client, execution_factory, execution):
    response = client.post(
        "api/v1/executions", json=execution_factory.stub(name=execution.name).__dict__
    )

    assert response.status_code == 409


def test_retrieve_execution_by_id(client, execution):
    response = client.get(f"api/v1/executions/{execution.id}")

    assert response.status_code == 200


def test_update_execution(client, execution, execution_factory):
    response = client.put(
        f"api/v1/executions/{execution.id}", json=execution_factory.stub().__dict__
    )

    assert response.status_code == 200


def test_delete_execution(client, execution):
    response = client.delete(f"api/v1/executions/{execution.id}")

    assert response.status_code == 200
