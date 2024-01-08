import uuid

INVALID_REPOSITORY_ID = uuid.uuid4()


def test_create_repository(client, repository_factory):
    response = client.post(
        "api/v1/repositories", json=repository_factory.stub().__dict__
    )

    assert response.status_code == 201


def test_create_repository_with_existing_name(client, repository_factory, repository):
    response = client.post(
        "api/v1/repositories",
        json=repository_factory.stub(name=repository.name).__dict__,
    )

    assert response.status_code == 409


def test_retrieve_repository_by_id(client, repository):
    response = client.get(f"api/v1/repositories/{repository.id}")

    assert response.status_code == 200


def test_update_repository(client, repository, repository_factory):
    response = client.put(
        f"api/v1/repositories/{repository.id}", json=repository_factory.stub().__dict__
    )

    assert response.status_code == 200


def test_delete_repository(client, repository):
    response = client.delete(f"api/v1/repositories/{repository.id}")

    assert response.status_code == 200
