def test_add_todo(todo_page, screenshot_helper):
    try:
        todo_page.add_todo("Shopping")
        todo_page.expect_todo_visible("Shopping")
    except Exception:
        screenshot_helper("test_add_todo")
        raise


def test_complete_todo(todo_page, screenshot_helper):
    try:
        todo_page.add_todo("Shopping")
        todo_page.complete_todo("Shopping")
        todo_page.expect_completed_count(1)
        todo_page.expect_footer_text("0 items left")
    except Exception:
        screenshot_helper("test_complete_todo")
        raise

def test_delete_todo(todo_page, screenshot_helper):
    try:
        todo_page.add_todo("Shopping")
        todo_page.delete_todo("Shopping")
        todo_page.expect_todo_count(0)
    except Exception:
        screenshot_helper("test_delete_todo")
        raise

def test_filter_active_todos(todo_page, screenshot_helper):
    try:
        for item in ["Shopping", "Cleaning", "Reading"]:
            todo_page.add_todo(item)
        todo_page.expect_todo_count(3)
        todo_page.complete_todo("Shopping")
        todo_page.expect_completed_count(1)
        todo_page.filter_by("Active")
        todo_page.expect_url_contains(r".*#/active")
        todo_page.expect_todo_count(2)
    except Exception:
        screenshot_helper("test_filter_active_todos")
        raise

def test_edit_todo(todo_page, screenshot_helper):
    try:
        todo_page.add_todo("Shopping")
        todo_page.edit_todo("Shopping", "Buy fruits and vegetables")
        todo_page.expect_todo_visible("Buy fruits and vegetables")
    except Exception:
        screenshot_helper("test_edit_todo")
        raise