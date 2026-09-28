#authentication tests using POST /api/login: (1) valid credentials returning a token,
# (2) missing password returning 400 with an error message.
#W6-1- Annotate 5 existing tests with Allure decorators; generate and review the Allure HTML report locally;
# add severity levels

import allure

@allure.feature("Authentication")
@allure.story("Login")
class TestAuth:
    @allure.title("POST /login with valid credentials returns a token")
    @allure.severity(allure.severity_level.BLOCKER)
    def test_login_valid_credentials_returns_token(self, session):
        # eve.holt@reqres.in / pistol is reqres's documented "always works" test account.
        payload = {"email": "eve.holt@reqres.in", "password": "pistol"}

        with allure.step("Send POST /Login with valid credentials"):
            response = session.post("/login", json=payload)

        with allure.step("Assert status code is 200"):
            assert response.status_code == 200, (
            f"Expected 200, got {response.status_code}: {response.text}"
        )

        with allure.step("Assert a non empty token is returned"):
            body = response.json()
        allure.attach(
           response.text, name="Response body" ,
            attachment_type=allure.attachment_type.JSON,
        )
        assert body.get("token"), f"Expected a non-empty token, got: {body}"

    def test_login_missing_password_returns_400(self, session):
        payload = {"email": "peter@klaven"}  # no password
        response = session.post("/login", json=payload)
        assert response.status_code == 400, (
            f"Expected 400, got {response.status_code}: {response.text}"
        )
        body = response.json()
        assert body.get("error"), f"Expected an error message, got: {body}"