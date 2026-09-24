#Add JSON schema validation to all response tests;
#assert required keys, data types, and response time under 2 seconds
# GET /api/users
import re
from jsonschema import validate
from config import API_BASE_URL
from api.schema import GET_USERS_LIST_SCHEMA, GET_SINGLE_USER_SCHEMA, CREATE_USER_SCHEMA, UPDATE_USER_SCHEMA

MAX_RESPONSE_TIME = 2.0  # in seconds

class TestGetUsers:
    def test_get_users_status_code(self, session):
        response = session.get(f"{API_BASE_URL}/users", params={"page": 2})
        assert response.status_code == 200
        assert response.elapsed.total_seconds() < MAX_RESPONSE_TIME

    def test_get_users_response_body_structure(self, session):
        response = session.get(f"{API_BASE_URL}/users", params={"page": 2})
        body = response.json()

        validate(instance=body, schema=GET_USERS_LIST_SCHEMA)
        assert body["page"] == 2
        assert len(body["data"]) > 0
        assert response.elapsed.total_seconds() < MAX_RESPONSE_TIME

    def test_get_users_data_item_shape(self, session):
        response = session.get(f"{API_BASE_URL}/users", params={"page": 2})
        body = response.json()

        # schema already checks required keys + types for every item in "data",
        # these extra asserts spot-check the first item's format specifically
        validate(instance=body, schema=GET_USERS_LIST_SCHEMA)
        first_user = body["data"][0]
        assert re.match(r"^https?://", first_user["avatar"])
        assert "@" in first_user["email"]
        assert response.elapsed.total_seconds() < MAX_RESPONSE_TIME

    def test_get_single_user_found(self, session):
        response = session.get(f"{API_BASE_URL}/users/2")
        body = response.json()

        assert response.status_code == 200
        validate(instance=body, schema=GET_SINGLE_USER_SCHEMA)
        assert body["data"]["id"] == 2
        assert body["data"]["email"] == "janet.weaver@reqres.in"
        assert response.elapsed.total_seconds() < MAX_RESPONSE_TIME

    def test_get_single_user_not_found(self, session):
        response = session.get(f"{API_BASE_URL}/users/23")
        assert response.status_code == 404
        assert response.json() == {}
        assert response.elapsed.total_seconds() < MAX_RESPONSE_TIME

# POST /api/users
class TestCreateUser:
    def test_create_user(self, session):
        payload = {"name": "morpheus", "job": "leader"}
        response = session.post(f"{API_BASE_URL}/users", json=payload)
        body = response.json()

        assert response.status_code == 201
        validate(instance=body, schema=CREATE_USER_SCHEMA)
        assert body["name"] == payload["name"]
        assert body["job"] == payload["job"]
        assert response.elapsed.total_seconds() < MAX_RESPONSE_TIME

#PUT /api/users/:id
class TestUpdateUser:
    def test_update_user(self, session):
        payload = {"name": "morpheus", "job": "Zion resident"}
        response = session.put(f"{API_BASE_URL}/users/2", json=payload)
        body = response.json()

        assert response.status_code == 200
        validate(instance=body, schema=UPDATE_USER_SCHEMA)
        assert body["job"] == payload["job"]
        assert response.elapsed.total_seconds() < MAX_RESPONSE_TIME

#DELETE /api/users/:id
class TestDeleteUser:
    def test_delete_user(self, session):
        response = session.delete(f"{API_BASE_URL}/users/2")

        assert response.status_code == 204
        assert response.text == ""
        assert response.elapsed.total_seconds() < MAX_RESPONSE_TIME