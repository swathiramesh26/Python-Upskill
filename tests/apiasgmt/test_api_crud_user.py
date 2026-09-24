#GET /api/users— assert status 200, response time < 2s, and validate response body against a JSON schema
#POST /api/users— send a JSON payload, assert status 201, and verify the returned id and createdAt fields are present.
#PUT /api/users/{id}— update a user, assert status 200, and verify the updatedAt field is present in the response.
#DELETE /api/users/{id}— assert status 204 and empty response body.

import jsonschema

from api.schema import GET_USERS_LIST_SCHEMA, CREATE_USER_SCHEMA, UPDATE_USER_SCHEMA
from utils.schema_loader import load_schema
MAX_RESPONSE_TIME_SECONDS = 2.0

#GET: GET /api/users
class TestGetUsers:
    def test_get_users_status_time_and_schema(self, session):
        response = session.get("/users", params={"page": 2})

        assert response.status_code == 200, (
            f"Expected 200, got {response.status_code}: {response.text}"
        )
        elapsed = response.elapsed.total_seconds()
        assert elapsed < MAX_RESPONSE_TIME_SECONDS, (
            f"Response took {elapsed:.2f}s, expected < {MAX_RESPONSE_TIME_SECONDS}s"
        )
        jsonschema.validate(instance=response.json(), schema=GET_USERS_LIST_SCHEMA)

#POST: CREATE /api/users
class TestCreateUser:
    def test_create_user(self, session):
        payload = {"name": "morpheus", "job": "leader"}
        response = session.post("/users", json=payload)
        assert response.status_code == 201, (
            f"Expected 201, got {response.status_code}: {response.text}"
        )
        body = response.json()
        assert "id" in body, f"Response missing 'id': {body}"
        assert "createdAt" in body, f"Response missing 'createdAt': {body}"
        jsonschema.validate(instance=body, schema=CREATE_USER_SCHEMA)

#PUT: UPDATE /api/users{id}
class TestUpdateUser:
    def test_update_user(self, session):
        payload = {"name": "morpheus", "job": "zion resident"}
        response = session.put("/users/2", json=payload)
        assert response.status_code == 200, (
            f"Expected 200, got {response.status_code}: {response.text}"
        )
        body = response.json()
        assert "updatedAt" in body, f"Response missing 'updatedAt': {body}"
        jsonschema.validate(instance=body, schema=UPDATE_USER_SCHEMA)

#DELETE: Delete /api/user{id}
class TestDeleteUser:
    def test_delete_user(self, session):
        response = session.delete("/users/2")
        assert response.status_code == 204, (
            f"Expected 204, got {response.status_code}: {response.text}"
        )
        assert response.text == "", (
            f"Expected an empty response body, got: {response.text!r}"
        )
