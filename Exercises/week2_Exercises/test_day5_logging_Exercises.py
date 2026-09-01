import logging
import pytest

logger = logging.getLogger(__name__)

def add(a, b):
    return a + b

def login(username, password):
    valid_users = {"alice": "alice@123", "bob": "bob@456"}
    return valid_users.get(username) == password

def test_addition():
    logger.info("Starting test_addition")
    a, b = 2, 3
    result = add(a, b)
    logger.info(f"add({a}, {b}) returned {result}")
    assert result == 6, f"Expected add({a}, {b}) to be 5, but got {result}"

def test_login_success():
    logger.info("Starting test_login_success")
    username, password = "alice", "alice@123"
    result = login(username, password)
    logger.info(f"login('{username}', '***') returned {result}")
    assert result is True, f"Expected login for '{username}' to succeed, but it failed"

def test_login_failure():
    logger.info("Starting test_login_failure")
    username, password = "alice", "wrongpassword"
    result = login(username, password)
    logger.info(f"login('{username}', '***') returned {result}")
    assert result is False, (
        f"Expected login for '{username}' with an incorrect password to fail, "
        f"but it returned {result}"
    )

def test_string_upper():
    logger.info("Starting test_string_upper")
    text = "hello"
    result = text.upper()
    logger.info(f"'{text}'.upper() returned '{result}'")
    assert result == "HELLO", f"Expected '{text}'.upper() to be 'HELLO', but got '{result}'"

def test_list_length():
    logger.info("Starting test_list_length")
    items = [1, 2, 3]
    result = len(items)
    logger.info(f"len({items}) returned {result}")
    assert result == 3, f"Expected len({items}) to be 3, but got {result}"