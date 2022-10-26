import pytest
from src.testgate.auth.schemas import UpdateUserRequestModel, UpdateUserResponseModel

create_user_request_body = {"firstname": "abdullah",
                            "lastname": "deliogullari",
                            "email": "abdullahdeliogullari@yaani.com",
                            "password": "147258DsA&",
                            "verified": False,
                            "roles": [],
                            "teams": []}

authenticate_user_request_body = {"email": "abdullahdeliogullari@yaani.com",
                                  "password": "147258DsA&"}

update_user_request_body = {"firstname": "abdullah",
                            "lastname": "deliogullari",
                            "email": "abdullahdeliogullari@yaani.com",
                            "password": "147258DsA&",
                            "verified": False,
                            "roles": [],
                            "teams": []}

@pytest.fixture
def user(client, role):
    response = client.post("api/v1/user", json={"firstname": "abdullah",
                            "lastname": "deliogullari",
                            "email": "abdullahdeliogullari@yaani.com",
                            "password": "147258DsA&",
                            "verified": False,
                            "roles": ["Admin"],
                            "teams": []})

    assert response.status_code == 201

    return response.json()

@pytest.fixture
def auth(client, user):
    response = client.post("api/v1/user/auth", json={"email": "abdullahdeliogullari@yaani.com",
                                  "password": "147258DsA&"})

    assert response.status_code == 200

    return response.json()

class TestAuthService:

    def test_create_user(self, client):
        create_user_request_body = {"firstname": "abdullah",
                                    "lastname": "deliogullari",
                                    "email": "abdullahdeliogullari@yaani.com",
                                    "password": "147258DsA&",
                                    "verified": False,
                                    "roles": [],
                                    "teams": []}

        response = client.post("api/v1/user", json=create_user_request_body)

        assert response.status_code == 201

    def test_auth_user(self, client):
        create_user_request_body = {"firstname": "abdullah",
                                    "lastname": "deliogullari",
                                    "email": "abdullahdeliogullari@yaani.com",
                                    "password": "147258DsA&",
                                    "verified": False,
                                    "roles": [],
                                    "teams": []}

        response = client.post("api/v1/user", json=create_user_request_body)

        assert response.status_code == 201

        authenticate_user_request_body = {"email": "abdullahdeliogullari@yaani.com",
                                          "password": "147258DsA&"}

        response = client.post("api/v1/user/auth", json=authenticate_user_request_body)

        assert response.status_code == 200

    # @pytest.mark.parametrize('create_user_request_body', [create_user_request_body])
    # @pytest.mark.parametrize('authenticate_user_request_body', [authenticate_user_request_body])
    def test_retrieve_current_user_by_token(self, client, auth):

        headers = {"Authorization": f"bearer {auth['access_token']}"}
        response = client.get(f"api/v1/users/me", headers=headers)

        assert response.status_code == 200

    # @pytest.mark.parametrize('create_user_request_body', [create_user_request_body])
    def test_retrieve_user_by_id(self, client, user):

        response = client.get(f"api/v1/user/{user['id']}")

        assert response.status_code == 200

    # @pytest.mark.parametrize('create_user_request_body', [create_user_request_body])
    def test_search_user(self, client, user):
        params = {'firstname': 'abdullah'}
        response = client.get(f"api/v1/users", params=params)

        assert response.status_code == 200
        assert len(response.json()) == 1
        assert response.json()[0]['firstname'] == 'abdullah'
        assert response.json()[0]['lastname'] == 'deliogullari'
        assert response.json()[0]['email'] == 'abdullahdeliogullari@yaani.com'

    # @pytest.mark.parametrize('create_user_request_body', [create_user_request_body])
    # @pytest.mark.parametrize('authenticate_user_request_body', [authenticate_user_request_body])
    def test_update_current_user_by_token(self, client, auth):

        headers = {"Authorization": f"bearer {auth['access_token']}"}
        response = client.put(f"api/v1/users/me", headers=headers, json=update_user_request_body)

        status_code = response.status_code
        response_body: UpdateUserResponseModel = response.json()
        assert status_code == 200
        # assert response_body.firstname == update_user_request_body.get("firstname")
        # assert response_body.lastname == update_user_request_body.get("lastname")
        # assert response_body.email == update_user_request_body.get("email")

    # @pytest.mark.parametrize('create_user_request_body', [create_user_request_body])
    # @pytest.mark.parametrize('authenticate_user_request_body', [authenticate_user_request_body])
    def test_update_user(self, client, auth):

        response = client.put(f"api/v1/user/{auth['id']}", json=update_user_request_body)

        assert response.status_code == 200

    # @pytest.mark.parametrize('create_user_request_body', [create_user_request_body])
    # @pytest.mark.parametrize('authenticate_user_request_body', [authenticate_user_request_body])
    def test_delete_current_user_by_token(self, client, auth):

        headers = {"Authorization": f"bearer {auth['access_token']}"}
        response = client.delete(f"api/v1/user/me", headers=headers)

        assert response.status_code == 200

    # @pytest.mark.parametrize('create_user_request_body', [create_user_request_body])
    # @pytest.mark.parametrize('authenticate_user_request_body', [authenticate_user_request_body])
    def test_delete_user(self, client, auth):

        headers = {"Authorization": f"bearer {auth['access_token']}"}
        response = client.delete(f"api/v1/user/{auth['id']}", headers=headers)

        assert response.status_code == 200
