# negative tests:
# (1) GET /api/users/999 returning 404
# (2) POST /api/users with an empty body returning an appropriate error.

class TestNegative:
    def test_get_nonexistent_user_returns_404(self, session):
        response = session.get("/users/999")
        assert response.status_code == 404, (
            f"Expected 404, got {response.status_code}: {response.text}"
        )
        assert response.json() == {}, (
            f"Expected an empty JSON object, got: {response.json()}"
        )
    def test_create_user_with_empty_body(self, session):
        response = session.post("/users", json={})
        assert response.status_code == 201, (
            f"Expected 201 (reqres.in does not validate POST payloads), "
            f"got {response.status_code}: {response.text}"
        )
        body = response.json()
        assert "id" in body and "createdAt" in body, (
            f"Even an empty payload should still get id/createdAt: {body}"
        )
        assert "name" not in body and "job" not in body, (
            f"No name/job should appear since none were sent: {body}"
        )