from config import API_BASE_URL, BASE_URL_SAUCE

class TestUiWithApiSetup:
    def test_create_user_via_api(self, api_request_context: APIRequestContext, page):
        # ---- api step: create the data first, without browser ----
        payload = {"name": "morpheus", "job": "leader"}
        response = api_request_context.post(f"{API_BASE_URL}/users", data=payload)
        assert response.ok
        created_user = response.json()

        # ---- UI step: now drive the browser using data we just created ----
        page.goto(BASE_URL_SAUCE)
        assert page.title() != ""

        # In a real app you'd navigate to a page showing the created user,
        # e.g. page.goto(f"{APP_URL}/users/{created_user['id']}")
        # and assert page.locator(...).to_contain_text(created_user["name"])
        print(f"Created user via API: {created_user}")
