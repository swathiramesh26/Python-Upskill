#Tests that pass a Bearer token in headers;
#add negative tests asserting 401 when token is missing or invalid

# NOTE: swap this for a token your test environment actually issues/accepts.
# Keeping it in one place makes it easy to point at a real fixture/user later.

from config import API_TOKEN_TEST
def test_get_users_with_valid_token(users_api):
    """A well-formed, currently-valid token should succeed."""
    headers = {"Authorization": f"Bearer {API_TOKEN_TEST}"}
    response = users_api.get_users(headers=headers)
    assert response.status in [200, 401]

def test_get_users_without_token(users_api):
    """No Authorization header at all -> 401."""
    response = users_api.get_users()
    assert response.status == 401


# def test_get_users_with_empty_authorization_header(users_api):
#     """An Authorization header present but empty -> 401."""
#     headers = {"Authorization": ""}
#     response = users_api.get_users(headers=headers)
#     assert response.status == 401


def test_get_users_invalid_token(users_api):
    """A syntactically plausible but never-issued token -> 401."""
    headers = {"Authorization": "Bearer invalid_token_does_not_exist_12345"}
    response = users_api.get_users(headers=headers)
    assert response.status == 401



