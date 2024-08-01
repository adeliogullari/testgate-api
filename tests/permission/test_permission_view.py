from fastapi.testclient import TestClient
from src.testgate.permission.models import Permission
from tests.permission.conftest import PermissionFactory


def test_create_permission(
    client: TestClient, permission_factory: PermissionFactory
) -> None:
    response = client.post(
        "api/v1/permissions", json=permission_factory.stub().__dict__
    )

    assert response.status_code == 201


def test_create_permission_with_existing_email(
    client: TestClient, permission_factory: PermissionFactory, permission: Permission
) -> None:
    response = client.post(
        "api/v1/permissions",
        json=permission_factory.stub(name=permission.name).__dict__,
    )

    assert response.status_code == 409


def test_retrieve_permission_by_id(client: TestClient, permission: Permission) -> None:
    response = client.get(f"api/v1/permission/{permission.id}")

    assert response.status_code == 200


def test_update_permission(
    client: TestClient, permission_factory: PermissionFactory, permission: Permission
) -> None:
    response = client.put(
        f"api/v1/permission/{permission.id}", json=permission_factory.stub().__dict__
    )

    assert response.status_code == 200


def test_delete_permission(client: TestClient, permission: Permission) -> None:
    response = client.delete(f"api/v1/permission/{permission.id}")

    assert response.status_code == 200
