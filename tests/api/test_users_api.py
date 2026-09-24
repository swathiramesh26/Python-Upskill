# pytest tests for GET /users, POST /users, PUT /users/{id},
#DELETE /users/{id} — assert status codes and response bodies
# Pytest api tests for reqres. in — / api / users endpoints.

# Covers:
# GET / api / users?page = 2
# POST / api / users
# PUT / api / users / {id}
# DELETE / api / users / {id}

from config import API_BASE_URL
import re
# GET /api/users
class TestGetUsers:
    def test_get_users_status_code(self, session):
        response = session.get(f"{API_BASE_URL}/users", params={"page": 2})
        assert response.status_code == 200

    def test_get_users_response_body_structure(self, session):
        response = session.get(f"{API_BASE_URL}/users", params={"page": 2})
        body = response.json()

        # top-level pagination fields
        assert body["page"] == 2
        assert "per_page" in body
        assert "total" in body
        assert "total_pages" in body

        # data is a non-empty list of user records
        assert isinstance(body["data"], list)
        assert len(body["data"]) > 0

    def test_get_users_data_item_shape(self, session):
        response = session.get(f"{API_BASE_URL}/users", params={"page": 2})
        first_user = response.json()["data"][0]

        for field in ("id", "email", "first_name", "last_name", "avatar"):
            assert field in first_user

        assert re.match(r"^https?://", first_user["avatar"])
        assert "@" in first_user["email"]

    def test_get_single_user_found(self, session):
        response = session.get(f"{API_BASE_URL}/users/2")
        assert response.status_code == 200

        user = response.json()["data"]
        assert user["id"] == 2
        assert user["email"] == "janet.weaver@reqres.in"

    def test_get_single_user_not_found(self, session):
        response = session.get(f"{API_BASE_URL}/users/23")
        assert response.status_code == 404
        assert response.json() == {}

# POST / api / users
class TestCreateUser:
    def test_create_user_status_code(self, session):
        payload = {"name": "morpheus", "job": "leader"}
        response = session.post(f"{API_BASE_URL}/users", json=payload)
        assert response.status_code == 201

    def test_create_user_response_body(self, session):
        payload = {"name": "morpheus", "job": "leader"}
        response = session.post(f"{API_BASE_URL}/users", json=payload)
        body = response.json()

        # shows what we sent
        assert body["name"] == payload["name"]
        assert body["job"] == payload["job"]

        # plus generated fields
        assert "id" in body
        assert "createdAt" in body

    def test_create_user_content_type(self, session):
        payload = {"name": "morpheus", "job": "leader"}
        response = session.post(f"{API_BASE_URL}/users", json=payload)
        assert "application/json" in response.headers["Content-Type"]

# PUT /api/users/{id}
class TestUpdateUser:
    def test_update_user_status_code(self, session):
        payload = {"name": "morpheus", "job": "zion resident"}
        response = session.put(f"{API_BASE_URL}/users/2", json=payload)
        assert response.status_code == 200

    def test_update_user_response_body(self, session):
        payload = {"name": "morpheus", "job": "zion resident"}
        response = session.put(f"{API_BASE_URL}/users/2", json=payload)
        body = response.json()

        assert body["name"] == payload["name"]
        assert body["job"] == payload["job"]
        assert "updatedAt" in body

# DELETE /api/users/{id}
class TestDeleteUser:
    def test_delete_user_status_code(self, session):
        response = session.delete(f"{API_BASE_URL}/users/2")
        assert response.status_code == 204

    def test_delete_user_empty_body(self, session):
        response = session.delete(f"{API_BASE_URL}/users/2")
        assert response.text == ""

