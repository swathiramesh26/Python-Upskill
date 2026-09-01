import re
import pytest
from playwright.sync_api import Page, expect

URL = "https://demo.playwright.dev/todomvc"

@pytest.fixture
def three_todos(page: Page):
    """Setup: navigate + add 3 todos, mark 1 as completed."""
    page.goto(URL)
    new_todo = page.get_by_placeholder("What needs to be done?")

    for item in ["Shopping", "Washing", "Cleaning"]:
        new_todo.press_sequentially(item, delay=50)
        new_todo.press("Enter")

    page.locator(".todo-list li", has_text="Cleaning").locator(".toggle").check()

    yield page

# 1. Element visibility
def test_heading_visiblity(three_todos: Page):
    page = three_todos
    heading = page.get_by_role("heading", name="todos")
    expect(heading).to_be_visible()

# 2. Text content
def test_footer_count(three_todos: Page):
    page = three_todos
    footer_count = page.locator(".todo-count")
    expect(footer_count).to_have_text("2 items left")

# 3. URL after navigation
def test_url_after_active_filter(three_todos: Page):
    page = three_todos
    page.get_by_role("link", name="Active").click()
    expect(page).to_have_url(re.compile(r".*#/active"))

def test_url_after_completed_filter(three_todos: Page):
    page = three_todos
    page.get_by_role("link", name="Completed").click()
    expect(page).to_have_url(re.compile(r".*#/completed"))

# 4. Element count after filtering
def test_active_filter_shows_uncompleted_items(three_todos: Page):
    page = three_todos
    page.get_by_role("link", name="Active").click()
    expect(page.locator(".todo-list li")).to_have_count(2)

def test_completed_filter_shows_completed_items(three_todos: Page):
    page = three_todos
    page.get_by_role("link", name="Completed").click()
    expect(page.locator(".todo-list li")).to_have_count(1)
    expect(page.get_by_text("Cleaning")).to_be_visible()