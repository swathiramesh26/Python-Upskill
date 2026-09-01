import time
import allure
import pytest

def add(a, b):
    return a + b

def is_even(n):
    return n % 2 == 0

def test_add_1():
    time.sleep(0.2)
    assert add(1, 1) == 2

def test_add_2():
    time.sleep(0.2)
    assert add(2, 3) == 5

def test_add_3():
    time.sleep(0.2)
    assert add(-1, 1) == 0

def test_even_1():
    time.sleep(0.2)
    assert is_even(4) is True

def test_even_2():
    time.sleep(0.2)
    assert is_even(7) is False

def test_string_upper():
    time.sleep(0.2)
    assert "test".upper() == "TEST"

def test_string_lower():
    time.sleep(0.2)
    assert "TEST".lower() == "test"

def test_list_sum():
    time.sleep(0.2)
    assert sum([1, 2, 3, 4]) == 10

def test_list_max():
    time.sleep(0.2)
    assert max([5, 1, 9, 3]) == 9


@allure.feature("User Login")
def test_login_flow():
    with allure.step("Enter valid username and password"):
        username, password = "alice", "password123"

    with allure.step("Submit login form"):
        result = username == "alice" and password == "password123"

    with allure.step("Verify login succeeds"):
        assert result is True