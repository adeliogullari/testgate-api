def test_retrieve_suite_by_id(client, suite):
    response = client.get(f"api/v1/suite/{suite.id}")

    assert response.status_code == 200


def test_create_suite(client, suite_factory):
    response = client.post("api/v1/suite", json=suite_factory.stub().__dict__)

    assert response.status_code == 201


def test_update_suite(client, suite_factory, suite):
    response = client.put(
        f"api/v1/suite/{suite.id}", json=suite_factory.stub().__dict__
    )

    assert response.status_code == 200


def test_delete_suite(client, suite):
    response = client.delete(f"api/v1/suite/{suite.id}")

    assert response.status_code == 200
