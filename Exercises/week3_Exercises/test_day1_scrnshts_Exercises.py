from playwright.sync_api import sync_playwright

URL = "https://demo.playwright.dev/todomvc"
BROWSERS = ["chromium", "firefox", "webkit"]

with sync_playwright() as p:
    for browser_name in BROWSERS:
        print(f"Launching {browser_name}...")
        browser_type = getattr(p, browser_name)
        browser = browser_type.launch(headless=False)
        page = browser.new_page()
        page.goto(URL)
        page.wait_for_load_state("networkidle")
        page.wait_for_timeout(3000)

        screenshot_path = f"screenshot_{browser_name}.png"
        page.screenshot(path=screenshot_path)
        print(f"Saved {screenshot_path}")
        browser.close()

print("Done. Screenshots saved for all 3 browsers.")