from playwright.sync_api import sync_playwright

# Base class for all test classes
class BaseTest:
    def setup_method(self):
        self.playwright = sync_playwright().start()
        self.browser = self.playwright.chromium.launch(headless=False)
        print("Launching browser...")
        self.context = self.browser.new_context()
        self.page = self.context.new_page()

    def teardown_method(self):
        print("Closing browser...")
        self.context.close()
        self.browser.close()
        self.playwright.stop()
        print("Browser closed successfully...")

# Child test class for Google open
class Test(BaseTest):
   def test_valid_login(self):
        self.page.goto("https://www.google.com")
        print("Google opened successfully...")

