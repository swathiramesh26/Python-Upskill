"""
good_tests_a.py: Refactored version of bad_tests_a.py:
- setup/teardown extracted into fixtures (in conftest.py)
- login test parametrized with 3 valid + 2 invalid inputs
- custom markers: @pytest.mark.smoke, @pytest.mark.regression
- one marked with @pytest.mark.skip, and one with @pytest.mark.xfail
"""
import pytest

# ---------- Cart tests (use the shared 'cart' fixture) ----------
@pytest.mark.smoke
def test_add_single_item(cart):
    cart["items"].append("apple")
    assert len(cart["items"]) == 1

@pytest.mark.regression
def test_add_multiple_items(cart):
    cart["items"].append("apple")
    cart["items"].append("banana")
    assert len(cart["items"]) == 2, f"Expected 2 items, got {len(cart['items'])}"

@pytest.mark.regression
def test_remove_item(cart):
    cart["items"].append("apple")
    cart["items"].remove("apple")
    assert len(cart["items"]) == 0


@pytest.mark.regression
def test_cart_total_price(cart):
    cart["items"].append({"name": "apple", "price": 50})
    cart["items"].append({"name": "banana", "price": 30})
    total = sum(item["price"] for item in cart["items"])
    assert total == 80, f"Expected total 80, got {total}"

@pytest.mark.smoke
def test_cart_is_empty_initially(cart):
    assert len(cart["items"]) == 0, "New cart should start empty"

@pytest.mark.smoke
def test_user_is_logged_in(cart):
    assert cart["logged_in"] is True, f"Expected user '{cart['user']}' to be logged in"

# ---------- Parametrized login test (3 valid + 2 invalid inputs) ----------
@pytest.mark.regression
@pytest.mark.parametrize(
    "username, password, expected",
    [
        # 3 valid credentials
        ("alice", "alice@123", True),
        ("bob", "bob@456", True),
        ("carol", "happy2789", True),
        # 2 invalid credentials
        ("alice", "alice@1234", False),
        ("dave", "dave123", False),
    ],
)
def test_login(valid_users, username, password, expected):
    result = valid_users.get(username) == password
    assert result == expected, (
        f"Expected login({username}) to be {expected}, but got {result}"
    )

# ---------- Skip and xfail examples ----------
@pytest.mark.skip(reason="Feature not implemented yet: guest checkout")
def test_guest_checkout(cart):
    assert cart.get("guest_checkout_enabled") is True

@pytest.mark.xfail(reason="Bug raised for incorrect rejection due to trailing whitespace in username")
def test_login_with_trailing_whitespace(valid_users):
    result = valid_users.get("alice    ") == "alice@123"
    assert result is True