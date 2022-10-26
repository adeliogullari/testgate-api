import pytest
from src.testgate.auth.schemas import UpdateUserRequestModel, UpdateUserResponseModel

create_role_request_body = {"name": "Admin"}

update_role_request_body = {"name": "User"}

@pytest.fixture
def role(client):
    response = client.post("api/v1/role", json={"name": "Admin"})

    assert response.status_code == 201

    return response.json()


class TestRoleService:

    def test_create_role(self, client):
        create_role_request_body = {"name": "Admin"}

        response = client.post("api/v1/role", json=create_role_request_body)

        assert response.status_code == 201

    # @pytest.mark.parametrize('create_role_request_body', [create_role_request_body])
    def test_retrieve_role_by_id(self, client, role):
        response = client.get(f"api/v1/role/{role['id']}")

        assert response.status_code == 200

    # @pytest.mark.parametrize('create_role_request_body', [create_role_request_body])
    def test_search_role(self, client, role):
        params = {'name': 'Admin'}
        response = client.get(f"api/v1/roles", params=params)

        assert response.status_code == 200
        assert len(response.json()) == 1
        assert response.json()[0]['name'] == 'Admin'

    # @pytest.mark.parametrize('create_role_request_body', [create_role_request_body])
    def test_update_role(self, client, role):
        response = client.put(f"api/v1/role/{role['id']}", json=update_role_request_body)

        assert response.status_code == 200

    # @pytest.mark.parametrize('create_role_request_body', [create_role_request_body])
    def test_delete_role(self, client, role):
        response = client.delete(f"api/v1/role/{role['id']}")

        assert response.status_code == 200
