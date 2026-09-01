from playwright.sync_api import Page, expect

URL = "https://demo.playwright.dev/todomvc"


def test_deliberate_failure(page: Page):
    page.goto(URL)

    new_todo = page.get_by_placeholder("What needs to be done?")
    new_todo.fill("Buy groceries")
    new_todo.press("Enter")

    # Deliberately wrong expected text -- this WILL fail on purpose
    expect(page.locator(".todo-count")).to_have_text("2 items left")