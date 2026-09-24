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
import requests
import httpx
from playwright.sync_api import Playwright
from api.users_api import UsersAPI
from config import BASE_URL_MVC, API_BASE_URL, API_TOKEN
from utils.http import BaseURLSession


#@pytest.fixture(params=["chromium", "firefox"])

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
    browser = browser_type.launch(headless=False)
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

#-------------Week 4------------#
sys.path.insert(0, os.path.dirname(__file__))
from config import HEADLESS, API_BASE_URL

fake = Faker()

@pytest.fixture(params=["chromium", "firefox"])
def browser_type_name(request):
    return request.param

@pytest.fixture
def browser_instance(playwright, browser_type_name):
    browser_type = getattr(playwright, browser_type_name)
    browser = browser_type.launch(headless=HEADLESS)
    yield browser
    browser.close()

@pytest.fixture
def page(browser_instance):
    context = browser_instance.new_context()
    page = context.new_page()
    yield page
    context.close()

@pytest.fixture
def random_user():
    return {
        "first_name": fake.first_name(),
        "last_name": fake.last_name(),
        "zip_code": fake.postcode(),
    }
#----------Week 5 Task3---------#
@pytest.fixture()
def api_base_url(request):
    return API_BASE_URL

@pytest.fixture(scope="session")
def session():
    """Reuse a single requests.Session for connection"""
    s = requests.Session()
    yield s
    s.close()

#--------Week 5 Task4---------#

# @pytest.fixture
# def auth_headers():
#     """Headers with a valid Bearer token."""
#     return {"Authorization": f"Bearer {VALID_TOKEN}"}
#
# @pytest.fixture
# def no_auth_headers():
#     """Headers with no Authorization key at all."""
#     return {}
#
# @pytest.fixture(params=[
#     "", "Bearer", "expired_token",
# ])
# def invalid_auth_headers(request):
#     """Headers with various invalid Bearer tokens."""
#     return {"Authorization": f"Bearer {request.param}"}

@pytest.fixture
def users_api(api_request_context):
    return UsersAPI(api_request_context)

#--------Week 5 Task5---------#

@pytest.fixture(scope="session")
def client():
    """Reuse a single httpx.Client for connection similar to requests.Session """
    with httpx.Client(base_url=API_BASE_URL, timeout=10.0) as c:
        yield c

#---------Test UI via api------#
@pytest.fixture(scope="session")
def api_request_context(playwright: Playwright):
    """A Playwright APIRequestContext for making direct HTTP calls,
    independent of any browser/page."""
    context = playwright.request.new_context(base_url=API_BASE_URL)
    yield context
    context.dispose()

#-------Week 5 Asgmt------#
@pytest.fixture(scope="session")
def session():
    """
    requests.Session pre-configured with base_url (so tests use relative
    paths like `session.get("/users")`) and, if API_TOKEN is set, an
    x-api-key header on every request.
    """
    s = BaseURLSession(API_BASE_URL)
    if API_TOKEN:
        s.headers.update({"x-api-key": API_TOKEN})
    yield s
    s.close()