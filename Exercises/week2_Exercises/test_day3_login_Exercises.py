import time
import pytest


def login(username, password):
    valid_users = {
        "alice": "alice@123",
        "bob": "bob@456",
        "carol": "happy2789",
    }
    # Assuming Known bug exists for usernames with trailing whitespace are incorrectly rejected
    # even when the password is correct. Tracked in BUG-101.
    if username in valid_users and valid_users[username] == password:
        return True
    return False


@pytest.mark.parametrize(
 "username, password, expected",
    [
        # 3 valid credentials
        ("alice", "alice@123", True),
        ("bob", "bob@456", True),
        ("carol", "happy2789", True),
        # 2 invalid credentials
        ("alice", "alice@112", False),
        ("dave", "password123", False),
    ],
)
def test_login(username, password, expected):
    assert login(username, password) == expected


@pytest.mark.slow
def test_login_under_heavy_load():
    time.sleep(2)
    assert login("alice", "alice@123") is True


@pytest.mark.xfail(reason="BUG-101: trailing whitespace in username incorrectly rejected")
def test_login_with_trailing_whitespace_username():
    assert login("alice  ", "alice@123") is True