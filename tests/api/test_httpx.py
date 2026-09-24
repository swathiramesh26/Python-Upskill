from config import API_BASE_URL
#Rewrite 3 requests tests using httpx; use playwright.
#request in a UI test to set up data via API before the browser step
MAX_RESPONSE_TIME = 2.0  # in seconds

class TestUsersHttpx:
    def test_get_users_httpx(self, client):
        response = client.get("/users", params={"page": 2})
        assert response.status_code == 200
        assert response.elapsed.total_seconds() < MAX_RESPONSE_TIME

        body = response.json()
        assert body["page"] == 2
        assert len(body["data"]) > 0

    def test_create_user_httpx(self, client):
        payload = {"name": "morpheus", "job": "leader"}
        response = client.post("/users", json=payload)
        body = response.json()

        assert response.status_code == 201
        assert body["name"] == payload["name"]
        assert body["job"] == payload["job"]
        assert "id" in body
        assert response.elapsed.total_seconds() < MAX_RESPONSE_TIME

    def test_update_user_httpx(self, client):
        payload = {"name": "morpheus", "job": "zion resident"}
        response = client.put("/users/2", json=payload)
        body = response.json()

        assert response.status_code == 200
        assert body["job"] == payload["job"]
        assert "updatedAt" in body
        assert response.elapsed.total_seconds() < MAX_RESPONSE_TIME