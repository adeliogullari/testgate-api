import uuid
from fastapi.testclient import TestClient
from src.testgate.repository.models import Repository
from tests.repository.conftest import RepositoryFactory

INVALID_REPOSITORY_ID = uuid.uuid4()


async def test_create_repository(
    client: TestClient, repository_factory: RepositoryFactory
) -> None:
    response = client.post(
        "api/v1/repositories", json=repository_factory.stub().__dict__
    )

    assert response.status_code == 201


async def test_create_repository_with_existing_name(
    client: TestClient, repository_factory: RepositoryFactory, repository: Repository
) -> None:
    response = client.post(
        "api/v1/repositories",
        json=repository_factory.stub(name=repository.name).__dict__,
    )

    assert response.status_code == 409


async def test_retrieve_repository_by_id(
    client: TestClient, repository: Repository
) -> None:
    response = client.get(f"api/v1/repositories/{repository.id}")

    assert response.status_code == 200


async def test_update_repository(
    client: TestClient, repository: Repository, repository_factory: RepositoryFactory
) -> None:
    response = client.put(
        f"api/v1/repositories/{repository.id}", json=repository_factory.stub().__dict__
    )

    assert response.status_code == 200


async def test_delete_repository(client: TestClient, repository: Repository) -> None:
    response = client.delete(f"api/v1/repositories/{repository.id}")

    assert response.status_code == 200
