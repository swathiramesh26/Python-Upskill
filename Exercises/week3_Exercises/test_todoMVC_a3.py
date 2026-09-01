import re
from playwright.sync_api import Page, expect

URL = "https://demo.playwright.dev/todomvc"

# 1. add a new todo item, and assert
def test_add_todo(page: Page):
    page.goto(URL)
    new_todo = page.get_by_placeholder("What needs to be done?")
    new_todo.fill("Shopping")
    new_todo.press("Enter")
    expect(page.get_by_text("Shopping")).to_be_visible()
# 2. Complete Todo: Add a todo, mark it as complete, moves to the completed state and the active count decrements.
def test_complete_todo(page: Page):
    page.goto(URL)
    new_todo = page.get_by_placeholder("What needs to be done?")
    new_todo.fill("Shopping")
    new_todo.press("Enter")
    todo_item = page.locator(".todo-list li", has_text="Shopping")
    expect(todo_item).to_be_visible()
    todo_item.locator(".toggle").check()
    expect(todo_item).to_have_class(re.compile("completed"))
    expect(page.locator(".todo-count")).to_have_text("0 items left")
# 3. Delete Todo: Add a todo, hover over it to reveal the delete button, click it, and assert the list is empty.
def test_delete_todo(page: Page):
    page.goto(URL)
    new_todo = page.get_by_placeholder("What needs to be done?")
    new_todo.fill("Shopping")
    new_todo.press("Enter")
    todo_item = page.locator(".todo-list li", has_text="Shopping")
    expect(todo_item).to_be_visible()
    todo_item.hover()
    todo_item.locator(".destroy").click()
    expect(page.locator(".todo-list li")).to_have_count(0)
#4. Filter Todos: Add 3 todos, complete 1, click the 'Active' filter, assert only 2 items are visible.
def test_filter_active_todos(page: Page):
    page.goto(URL)
    new_todo = page.get_by_placeholder("What needs to be done?")
    items = ["Shopping", "Cleaning", "Reading"]
    for item in items:
      new_todo.fill(item)
      new_todo.press("Enter")
    expect(page.locator(".todo-list li")).to_have_count(3)
    page.locator(".todo-list li", has_text="Shopping").locator(".toggle").check()
    expect(page.locator(".todo-list li.completed")).to_have_count(1)
    page.get_by_role("link", name="Active").click()
    expect(page).to_have_url(re.compile(r".*#/active"))
    expect(page.locator(".todo-list li")).to_have_count(2)
#5. Edit Todo: Double-click a todo to enter edit mode, change the text, press Enter, and assert the updated text is displayed.
def test_edit_todo(page: Page):
    page.goto(URL)
    new_todo = page.get_by_placeholder("What needs to be done?")
    new_todo.fill("Shopping")
    new_todo.press("Enter")

    todo_item = page.locator(".todo-list li", has_text="Shopping")
    expect(todo_item).to_be_visible()
    todo_item.dblclick()
    edit_box = todo_item.locator(".edit")
    expect(edit_box).to_be_visible()
    edit_box.fill("Buy fruits and vegetables")
    edit_box.press("Enter")
    expect(page.get_by_text("Buy fruits and vegetables")).to_be_visible()