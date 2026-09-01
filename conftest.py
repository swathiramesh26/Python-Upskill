"""
conftest.py
Shared fixtures available to all test files in this directory.
Extracts the duplicated cart setup/teardown logic from bad_tests_a.py
into a single, reusable, function-scoped fixture.
"""
import os
import sys
import pytest
import json
from faker import Faker
from pages.todo_page import TodoPage

@pytest.fixture(scope="function")
def cart():
    # ---- Setup ----
    print("\n[SETUP] Creating a fresh cart for 'alice'")
    test_cart = {"items": [], "user": "alice", "logged_in": True}

    yield test_cart

    # ---- Teardown ----
    print("\n[TEARDOWN] Clearing cart for 'alice'")
    test_cart["items"].clear()


@pytest.fixture(scope="function")
def valid_users():
    # ---- Setup ----
    print("\n[SETUP] Loading valid_users dictionary")
    users = {"alice": "alice@123", "bob": "bob@456", "carol": "happy2789"}

    yield users

    # ---- Teardown ----
    print("\n[TEARDOWN] Discarding valid_users dictionary")

#----- Playwright a3 ------#
@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item):
        """Stores the test's pass/fail outcome on the test item itself,
        so fixtures can inspect it after the test body has run."""
        outcome = yield
        rep = outcome.get_result()
        setattr(item, f"rep_{rep.when}", rep)

@pytest.fixture
def screenshot_on_failure(request, page):
        """Runs around every test automatically. If the test failed,
        saves a screenshot named after the test into screenshots/."""
        yield
        if request.node.rep_call.failed:
            os.makedirs("screenshots", exist_ok=True)
            screenshot_path = f"screenshots/{request.node.name}.png"
            page.screenshot(path=screenshot_path)
            print(f"\n[SCREENSHOT SAVED] {screenshot_path}")

#------Page Object Model 1--------#
sys.path.insert(0, os.path.dirname(__file__))
@pytest.fixture
def todo_page(page):
    pom = TodoPage(page)
    pom.goto()
    return pom

@pytest.fixture
def screenshot_helper(page):
    def _capture(test_name):
        os.makedirs("screenshots", exist_ok=True)
        screenshot_path = f"screenshots/{test_name}.png"
        page.screenshot(path=screenshot_path)
        print(f"\n[SCREENSHOT SAVED] {screenshot_path}")
    return _capture

#---------Faker Task4 Ex3----------#
fake = Faker()
@pytest.fixture
def dynamic_todos():
    """Generates 5 random todo items using Faker, sentence length defaults to 6."""
    return [fake.sentence().rstrip(".") for i in range(5)]

@pytest.fixture
def static_todos():
    """Loads a fixed list of todo items from a JSON file."""
    with open("testdata/todo.json") as f:
        data = json.load(f)
    return data["todo"]

#-------------xdist Task4 Ex4------------#
"""browsers to test with"""
# @pytest.fixture(params=["chromium", "firefox"])
# def browser_type_name(request):
#     """Parametrized directly via params= on the fixture decorator."""
#     return request.param
"""Open Browser"""
@pytest.fixture
def browser_instance(playwright, browser_name):
    """Launches the actual browser matching browser_name,
    and cleans up after the test finishes."""
    browser_type = getattr(playwright, browser_name)
    browser = browser_type.launch(headless=True)
    yield browser
    browser.close()
"""Open tab in browser"""
@pytest.fixture
def page(browser_instance):
    """Overrides pytest-playwright's default page fixture so every test
    gets a page from OUR parametrized browser_instance, not a fixed one."""
    context = browser_instance.new_context()
    page = context.new_page()
    yield page
    context.close()