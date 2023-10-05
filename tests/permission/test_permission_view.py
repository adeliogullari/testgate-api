def test_create_permission(client, permission_factory):

    response = client.post("api/v1/permissions", json=permission_factory.stub().__dict__)

    assert response.status_code == 201


def test_create_permission_with_existing_email(client, permission_factory, permission):

    response = client.post("api/v1/permissions", json=permission_factory.stub(name=permission.name).__dict__)

    assert response.status_code == 409


def test_retrieve_permission_by_id(client, user):

    response = client.get(f"api/v1/users/{user.id}")

    assert response.status_code == 200


def test_update_permission(client, permission, permission_factory):

    response = client.put(f"api/v1/permission/{permission.id}", json=permission_factory.stub().__dict__)

    assert response.status_code == 200


def test_delete_permission(client, permission):

    response = client.delete(f"api/v1/permission/{permission.id}")

    assert response.status_code == 200
