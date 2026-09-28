#GET /api/users— assert status 200, response time < 2s, and validate response body against a JSON schema
#POST /api/users— send a JSON payload, assert status 201, and verify the returned id and createdAt fields are present.
#PUT /api/users/{id}— update a user, assert status 200, and verify the updatedAt field is present in the response.
#DELETE /api/users/{id}— assert status 204 and empty response body.
#W6-1- Annotate 5 existing tests with Allure decorators; generate and review the Allure HTML report locally;
# add severity levels

import allure
import jsonschema
from api.schema import GET_USERS_LIST_SCHEMA, CREATE_USER_SCHEMA, UPDATE_USER_SCHEMA
from utils.schema_loader import load_schema
MAX_RESPONSE_TIME_SECONDS = 2.0


@allure.feature("Users API")
@allure.story("Get Users")
#GET: GET /api/users
class TestGetUsers:
    @allure.title("GET /api/users returns 200 under 2s, with matching schema")
    @allure.severity(allure.severity_level.NORMAL)
    def test_get_users_status_time_and_schema(self, session):
        with allure.step("Send GET /users?page=2"):
            response = session.get("/users", params={"page": 2})

        with allure.step("Assert status code is 200"):
            assert response.status_code == 200, (
            f"Expected 200, got {response.status_code}: {response.text}"
        )

        with allure.step("Assert response time is under 2s"):
            elapsed = response.elapsed.total_seconds()
            allure.attach(
                str(elapsed), name="Response time (s)",
                attachment_type=allure.attachment_type.TEXT,
            )

            assert elapsed < MAX_RESPONSE_TIME_SECONDS, (
                f"Response took {elapsed:.2f}s, expected < {MAX_RESPONSE_TIME_SECONDS}s"
            )

        with allure.step("Validate response body against schema"):
            allure.attach(
                response.text, name="Response body",
                attachment_type=allure.attachment_type.JSON,
            )

        jsonschema.validate(instance=response.json(), schema=GET_USERS_LIST_SCHEMA)

#POST: CREATE /api/users
@allure.story("Create User")
class TestCreateUser:
    @allure.title("POST /api/creates user and returns id + createdAt")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_create_user(self, session):
        payload = {"name": "morpheus", "job": "leader"}

        with allure.step("Send POST /users with payload"):
            allure.attach(
                str(payload), name="Request payload",
                attachment_type=allure.attachment_type.JSON,
            )
        response = session.post("/users", json=payload)

        with allure.step("Assert status code is 201"):
            assert response.status_code == 201, (
                f"Expected 201, got {response.status_code}: {response.text}"
        )

        with allure.step("Assert id and createdAt are present"):
            body = response.json()
            allure.attach(
                response.text, Name= "Response body",
                attachment_type=allure.attachment_type.JSON,
            )
            assert "id" in body, f"Response missing 'id': {body}"
            assert "createdAt" in body, f"Response missing 'createdAt': {body}"

        with allure.step("Validate response body against schema"):
            jsonschema.validate(instance=body, schema=CREATE_USER_SCHEMA)

#PUT: UPDATE /api/users{id}
@allure.story("Update User")
class TestUpdateUser:
    @allure.title("PUT /users/{id} updates user and returns updatedAt")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_update_user(self, session):
        payload = {"name": "morpheus", "job": "zion resident"}

        with allure.step("Send PUT/users/2 with payload"):
            allure.attach(
                str(payload), Name= "Request payload",
                attachment_type=allure.attachment_type.JSON,
            )
        response = session.put("/users/2", json=payload)

        with allure.step("Assert status code is 200"):
            assert response.status_code == 200, (
                f"Expected 200, got {response.status_code}: {response.text}"
            )
        with allure.step("Assert updatedAt is present"):
            body = response.json()
            allure.attach(
                response.text, Name= "Response body",
                attachment_type=allure.attachment_type.JSON,
            )
            assert "updatedAt" in body, f"Response missing 'updatedAt': {body}"

        with allure.step("Validate response body against schema"):
            jsonschema.validate(instance=body, schema=UPDATE_USER_SCHEMA)

#DELETE: Delete /api/user{id}
@allure.story("Delete User")
class TestDeleteUser:
    @allure.title("DELETE /users/{id} returns 204 with an empty body")
    @allure.severity(allure.severity_level.MINOR)
    def test_delete_user(self, session):
        with allure.step("Send DELETE /users/2"):
            response = session.delete("/users/2")

        with allure.step("Assert status code is 204"):
            assert response.status_code == 204, (
                f"Expected 204, got {response.status_code}: {response.text}"
        )
        with allure.step("Assert response body is empty"):
            assert response.text == "", (
                f"Expected an empty response body, got: {response.text!r}"
        )
