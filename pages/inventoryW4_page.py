from playwright.sync_api import expect
from pages.baseW4_page import BasePage


class InventoryPage(BasePage):
    INVENTORY_LIST = ".inventory_list"
    CART_BADGE = ".shopping_cart_badge"
    ADD_TO_CART_BUTTON_TEMPLATE = "button[data-test='add-to-cart-{item_name}']"

    def add_item_to_cart(self, item_name: str):
        button = self.page.locator(self.ADD_TO_CART_BUTTON_TEMPLATE.format(item_name=item_name))
        button.click()
        return self

    def expect_loaded(self):
        expect(self.page.locator(self.INVENTORY_LIST)).to_be_visible()

    def expect_cart_count(self, count: int):
        expect(self.page.locator(self.CART_BADGE)).to_have_text(str(count))