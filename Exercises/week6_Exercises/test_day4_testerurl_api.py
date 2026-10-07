"""
API tests for https://thinking-tester-contact-list.herokuapp.com

Endpoints covered:
  POST /users        -- sign up
  POST /users/login   -- login
  POST /contacts       -- create contact (requires Bearer token)
  GET  /contacts       -- list contacts (requires Bearer token)
"""

import allure
from jsonschema import validate
from api.schema import USER_AUTH_SCHEMA, CONTACT_SCHEMA, CONTACTS_LIST_SCHEMA

@allure.feature("Contact List API")
class TestUserSignup:
    @allure.story("Sign Up")
    @allure.title("POST /users with a new email creates an account and returns a token")
    @allure.severity(allure.severity_level.BLOCKER)
    def test_signup_returns_token_and_user(self, api_session, api_tester_url, new_user):
        with allure.step("POST /users with a fresh, unique payload"):
            allure.attach(str(new_user), name="Request payload", attachment_type=allure.attachment_type.JSON)
            response = api_session.post(f"{api_tester_url}/users", json=new_user)

        with allure.step("Assert 201 Created"):
            assert response.status_code == 201, (
                f"Expected 201, got {response.status_code}: {response.text}"
            )

        with allure.step("Assert a token and matching user email are returned"):
            body = response.json()
            allure.attach(response.text, name="Response body", attachment_type=allure.attachment_type.JSON)
            validate(instance=body, schema=USER_AUTH_SCHEMA)
            assert body.get("token"), f"Expected a non-empty token, got: {body}"
            assert body["user"]["email"] == new_user["email"]


@allure.feature("Contact List API")
class TestLogin:
    @allure.story("Login")
    @allure.title("POST /users/login with valid credentials returns a token")
    @allure.severity(allure.severity_level.BLOCKER)
    def test_login_with_valid_credentials(self, api_session, api_tester_url, registered_user):
        with allure.step("POST /users/login with the registered account's credentials"):
            payload = {
                "email": registered_user["email"],
                "password": registered_user["password"],
            }
            response = api_session.post(f"{api_tester_url}/users/login", json=payload)

        with allure.step("Assert 200 and a non-empty token"):
            assert response.status_code == 200, (
                f"Expected 200, got {response.status_code}: {response.text}"
            )
            body = response.json()
            allure.attach(response.text, name="Response body", attachment_type=allure.attachment_type.JSON)
            validate(instance=body, schema=USER_AUTH_SCHEMA)
            assert body.get("token"), f"Expected a non-empty token, got: {body}"

    @allure.story("Login")
    @allure.title("POST /users/login with invalid credentials returns 401")
    @allure.severity(allure.severity_level.NORMAL)
    def test_login_with_invalid_credentials_returns_401(self, api_session, api_tester_url):
        with allure.step("POST /users/login with bogus credentials"):
            payload = {"email": "nobody.not.registered@example.com", "password": "wrong-password"}
            response = api_session.post(f"{api_tester_url}/users/login", json=payload)

        with allure.step("Assert 401 Unauthorized"):
            assert response.status_code == 401, (
                f"Expected 401, got {response.status_code}: {response.text}"
            )


@allure.feature("Contact List API")
class TestContacts:
    @allure.story("Create Contact")
    @allure.title("POST /contacts with a valid token creates a contact")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_create_contact_with_valid_token(
        self, api_session, api_tester_url, registered_user, new_contact
    ):
        with allure.step("POST /contacts with Bearer token from setup"):
            headers = {"Authorization": f"Bearer {registered_user['token']}"}
            allure.attach(str(new_contact), name="Request payload", attachment_type=allure.attachment_type.JSON)
            response = api_session.post(
                f"{api_tester_url}/contacts", json=new_contact, headers=headers
            )

        with allure.step("Assert 201 and the returned contact matches what was sent"):
            assert response.status_code == 201, (
                f"Expected 201, got {response.status_code}: {response.text}"
            )
            body = response.json()
            allure.attach(response.text, name="Response body", attachment_type=allure.attachment_type.JSON)
            validate(instance=body, schema=CONTACT_SCHEMA)
            assert body["firstName"] == new_contact["firstName"]
            assert body["email"] == new_contact["email"]

    @allure.story("List Contacts")
    @allure.title("GET /contacts with a valid token returns the user's contacts")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_get_contacts_includes_created_contact(
        self, api_session, api_tester_url, registered_user, new_contact
    ):
        headers = {"Authorization": f"Bearer {registered_user['token']}"}

        with allure.step("Create a contact to guarantee the list is non-empty"):
            create_response = api_session.post(
                f"{api_tester_url}/contacts", json=new_contact, headers=headers
            )
            assert create_response.status_code == 201, (
                f"Setup failed creating contact: {create_response.status_code} {create_response.text}"
            )

        with allure.step("GET /contacts"):
            response = api_session.get(f"{api_tester_url}/contacts", headers=headers)

        with allure.step("Assert 200 and the created contact is present in the list"):
            assert response.status_code == 200, (
                f"Expected 200, got {response.status_code}: {response.text}"
            )
            contacts = response.json()
            allure.attach(response.text, name="Response body", attachment_type=allure.attachment_type.JSON)
            assert any(c["email"] == new_contact["email"] for c in contacts), (
                f"Created contact not found in list: {contacts}"
            )