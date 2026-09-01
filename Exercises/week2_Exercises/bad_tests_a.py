
#duplicated setup logic, hardcoded values,no fixtures. E-commerce site that creates "cart" from the beginning.

def test_add_single_item():
    # duplicated setup
    cart = {"items": [], "user": "alice", "logged_in": True}
    cart["items"].append("apple")
    assert len(cart["items"]) == 1


def test_add_multiple_items():
    # duplicated setup
    cart = {"items": [], "user": "alice", "logged_in": True}
    cart["items"].append("apple")
    cart["items"].append("banana")
    assert len(cart["items"]) == 2


def test_remove_item():
    # duplicated setup
    cart = {"items": [], "user": "alice", "logged_in": True}
    cart["items"].append("apple")
    cart["items"].remove("apple")
    assert len(cart["items"]) == 0


def test_cart_total_price():
    # duplicated setup
    cart = {"items": [], "user": "alice", "logged_in": True}
    cart["items"].append({"name": "apple", "price": 50})
    cart["items"].append({"name": "banana", "price": 30})
    total = sum(item["price"] for item in cart["items"])
    assert total == 80


def test_cart_is_empty_initially():
    # duplicated setup
    cart = {"items": [], "user": "alice", "logged_in": True}
    assert len(cart["items"]) == 0


def test_user_is_logged_in():
    # duplicated setup
    cart = {"items": [], "user": "alice", "logged_in": True}
    assert cart["logged_in"] is True


def test_login_valid_credentials():
    # hardcoded values, duplicated setup
    username = "alice"
    password = "password123"
    valid_users = {"alice": "password123", "bob": "secret456"}
    assert valid_users.get(username) == password


def test_login_invalid_credentials():
    # hardcoded values, duplicated setup
    username = "alice"
    password = "wrongpassword"
    valid_users = {"alice": "password123", "bob": "secret456"}
    assert valid_users.get(username) != password