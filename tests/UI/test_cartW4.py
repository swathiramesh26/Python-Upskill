import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from pages.loginW4_page import LoginPage
from pages.inventoryW4_page import InventoryPage
from config import USERNAME, PASSWORD

def test_successful_login(page):
    loginW4_page = LoginPage(page).open()
    loginW4_page.login(USERNAME, PASSWORD)
    InventoryPage(page).expect_loaded()

def test_failed_login_invalid_credentials(page):
    loginW4_page = LoginPage(page).open()
    loginW4_page.login("invalid_user", "wrong_password")
    loginW4_page.expect_error_message("Username and password do not match")

def test_add_item_to_cart(page):
    loginW4_page = LoginPage(page).open()
    loginW4_page.login(USERNAME, PASSWORD)

    inventoryW4_page = InventoryPage(page)
    inventoryW4_page.expect_loaded()
    inventoryW4_page.add_item_to_cart("sauce-labs-backpack")
    inventoryW4_page.expect_cart_count(1)