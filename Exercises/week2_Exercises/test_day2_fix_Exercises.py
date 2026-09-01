import pytest

# fixture scope= session
@pytest.fixture(scope="session")
def db_connection():
    print("\n[SESSION] Setup - connecting to library database (runs ONCE)")
    connection = {"status": "connected", "host": "library-db.local"}
    yield connection
    print("[SESSION] Teardown - closing library database connection")

# fixture scope= module
@pytest.fixture(scope="module")
def Animation_catalog(db_connection):
    print("\n[MODULE] Setup - loading 'Animation' catalog (runs once per file)")
    catalog = {"category": "Animation", "db": db_connection["status"]}
    yield catalog
    print("[MODULE] Teardown - unloading 'Animation' catalog")

# fixture scope= function
@pytest.fixture(scope="function")
def book_checkout(Animation_catalog):
    print("\n[FUNCTION] Setup - issuing a fresh book checkout (runs before EACH test)")
    checkout = {"book": None, "catalog": Animation_catalog["category"], "returned": False}
    yield checkout
    print("[FUNCTION] Teardown - returning the book / clearing checkout record")


def test_checkout_book(book_checkout):
    print("[TEST] Running test_checkout_book")
    book_checkout["book"] = "How to Train Your Dragon"
    assert book_checkout["book"] == "How to Train Your Dragon"
    assert book_checkout["catalog"] == "Animation"


def test_return_book(book_checkout):
    print("[TEST] Running test_return_book")
    book_checkout["book"] = "2010"
    book_checkout["returned"] = True
    assert book_checkout["returned"] is True
    assert book_checkout["catalog"] == "Animation"