import pytest
def add(a, b):
    return a + b

def test_add_positive():
    assert add(2, 3) == 6

def test_add_negative():
    assert add(-1, -1) == -2

def test_add_zero():
    assert add(0, 5) == 5

def test_string_upper():
    assert "hello".upper() == "HELLO"

def test_list_length():
    assert len([1, 2, 3]) == 3