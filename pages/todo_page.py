from playwright.sync_api import Page, expect
from config import BASE_URL_MVC

class TodoPage:
    URL = BASE_URL_MVC

    # ---------- Locator constants ----------
    NEW_TODO_INPUT = "input.new-todo"
    TODO_ITEMS = ".todo-list li"
    TODO_ITEM_COMPLETED = ".todo-list li.completed"
    TOGGLE_CHECKBOX = ".toggle"
    DESTROY_BUTTON = ".destroy"
    EDIT_INPUT = ".edit"
    TODO_COUNT = ".todo-count"

    def __init__(self, page: Page):
        self.page = page

    def goto(self):
        self.page.goto(self.URL)
        return self

    # ---------- Locator helpers ----------
    def new_todo_input(self):
        return self.page.locator(self.NEW_TODO_INPUT)

    def todo_items(self):
        return self.page.locator(self.TODO_ITEMS)

    def todo_item(self, text: str):
        return self.page.locator(self.TODO_ITEMS, has_text=text)

    def completed_items(self):
        return self.page.locator(self.TODO_ITEM_COMPLETED)

    def todo_count_text(self):
        return self.page.locator(self.TODO_COUNT)

    def filter_link(self, name: str):
        return self.page.get_by_role("link", name=name)

    # ---------- Actions ----------
    def add_todo(self, text: str):
        todo_input = self.new_todo_input()
        todo_input.press_sequentially(text, delay=50)
        todo_input.press("Enter")
        return self

    def complete_todo(self, text: str):
        item = self.todo_item(text)
        expect(item).to_be_visible()
        item.locator(self.TOGGLE_CHECKBOX).check()
        return self

    def delete_todo(self, text: str):
        item = self.todo_item(text)
        expect(item).to_be_visible()
        item.hover()
        delete_button = item.locator(self.DESTROY_BUTTON)
        expect(delete_button).to_be_visible()
        delete_button.click()
        return self

    def edit_todo(self, old_text: str, new_text: str):
        item = self.todo_item(old_text)
        expect(item).to_be_visible()
        item.dblclick()
        edit_box = item.locator(self.EDIT_INPUT)
        expect(edit_box).to_be_visible()
        edit_box.fill(new_text)
        edit_box.press("Enter")
        return self

    def filter_by(self, name: str):
        self.filter_link(name).click()
        return self

    # ---------- Assertions ----------
    def expect_todo_visible(self, text: str):
        expect(self.page.get_by_text(text)).to_be_visible()

    def expect_todo_count(self, count: int):
        expect(self.todo_items()).to_have_count(count)

    def expect_completed_count(self, count: int):
        expect(self.completed_items()).to_have_count(count)

    def expect_footer_text(self, text: str):
        expect(self.todo_count_text()).to_have_text(text)

    def expect_url_contains(self, fragment: str):
        import re
        expect(self.page).to_have_url(re.compile(fragment))