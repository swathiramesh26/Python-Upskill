from playwright.sync_api import Page, expect

URL = "https://demo.playwright.dev/todomvc"


def test_five_locator(page: Page):
    page.goto(URL)

    # A todo needs to exist first -- the footer only renders once
    # there's at least one item.
    new_todo = page.get_by_placeholder("What needs to be done?")
    new_todo.fill("Buy groceries")
    new_todo.press("Enter")

    # 1. get_by_role -- ARIA role + accessible name
    heading = page.get_by_role("heading", name="todos")
    expect(heading).to_be_visible()

    # 2. get_by_placeholder -- form control via placeholder text
    input_box = page.get_by_placeholder("What needs to be done?")
    expect(input_box).to_be_visible()

    # 3. get_by_text -- element via its visible text content
    todo_text_loc = page.get_by_text("Buy groceries")
    expect(todo_text_loc).to_be_visible()

    # 4. CSS locator -- plain CSS selector - picks first match
    first_todo_item = page.locator(".todo-list li").first
    expect(first_todo_item).to_be_visible()

    # 5. XPath locator -- XPath expression To find footer element
    footer = page.locator("xpath=//footer[contains(@class, 'footer')]")
    expect(footer).to_be_visible()