from fastapi.testclient import TestClient
from src.testgate.role.models import Role
from tests.role.conftest import RoleFactory


async def test_retrieve_role_by_id(client: TestClient, role: Role) -> None:
    response = client.get(f"api/v1/role/{role.id}")

    assert response.status_code == 200


async def test_search_role(client: TestClient, role: Role) -> None:
    response = client.get("api/v1/roles", params={"name": role.name})

    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["name"] == role.name


async def test_create_role(client: TestClient, role_factory: RoleFactory) -> None:
    response = client.post("api/v1/role", json=role_factory.stub().__dict__)

    assert response.status_code == 201


async def test_update_role(
    client: TestClient, role: Role, role_factory: RoleFactory
) -> None:
    response = client.put(f"api/v1/role/{role.id}", json=role_factory.stub().__dict__)

    assert response.status_code == 200


async def test_delete_role(client: TestClient, role: Role) -> None:
    response = client.delete(f"api/v1/role/{role.id}")

    assert response.status_code == 200
