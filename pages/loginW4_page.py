from playwright.sync_api import expect
from pages.baseW4_page import BasePage


class LoginPage(BasePage):
    URL = "https://www.saucedemo.com/"

    USERNAME_INPUT = "#user-name"
    PASSWORD_INPUT = "#password"
    LOGIN_BUTTON = "#login-button"
    ERROR_MESSAGE = "[data-test='error']"

    def open(self):
        self.goto(self.URL)
        return self

    def login(self, username: str, password: str):
        self.page.locator(self.USERNAME_INPUT).fill(username)
        self.page.locator(self.PASSWORD_INPUT).fill(password)
        self.page.locator(self.LOGIN_BUTTON).click()
        return self

    def expect_error_message(self, text: str):
        expect(self.page.locator(self.ERROR_MESSAGE)).to_contain_text("do not match")