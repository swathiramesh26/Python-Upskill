from playwright.sync_api import Page, expect

URL = "https://demo.playwright.dev/todomvc"


def test_todo_lifecycle(page: Page):
    page.goto(URL)

    new_todo = page.get_by_placeholder("What needs to be done?")
    todo_items = page.locator(".todo-list li")

    # 1. Add 3 items
    items = ["Shopping", "Cleaning", "Reading"]
    for item in items:
        new_todo.press_sequentially(item, delay=50)
        new_todo.press("Enter")

    expect(todo_items).to_have_count(3)

    # 2. Complete 2 of the 3 items
    for item in items[:2]:
        page.locator(".todo-list li", has_text=item).locator(".toggle").check()

    expect(page.locator(".todo-list li.completed")).to_have_count(2)

    # 3. Clear completed
    page.get_by_role("button", name="Clear completed").click()

    # 4. Assert remaining count
    expect(todo_items).to_have_count(1)
    expect(page.get_by_text(items[2])).to_be_visible()
    expect(page.locator(".todo-count")).to_contain_text("1 item left")