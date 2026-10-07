"""
UI tests for https://thinking-tester-contact-list.herokuapp.com
5 UI tests - Allure annotations and CI pipelines
"""

import allure
from pages.testerurl_ui_page import TesterUrlPage

@allure.feature("Contact List UI")
class TestSignup:
    @allure.story("Sign Up")
    @allure.title("Signing up with a new email creates an account and shows the contact list")
    @allure.severity(allure.severity_level.BLOCKER)
    def test_signup_creates_account(self, page, ui_tester_url, new_user):
        tester_page = TesterUrlPage(page)
        with allure.step("Go to the app and open the sign up form"):
            tester_page.navigate_to_login(ui_tester_url)
            tester_page.open_signup()

        with allure.step("Fill in the sign up form with unique user"):
            tester_page.signup(
                new_user["firstName"],
                new_user["lastName"],
                new_user["email"],
                new_user["password"]
            )

        with allure.step("Assert the account was created and the contact list is shown"):
            tester_page.wait_for_contact_list()
            allure.attach(page.url, name="Landed on URL", attachment_type=allure.attachment_type.TEXT)
            assert "contactList" in page.url


@allure.feature("Contact List UI")
class TestLogin:
    @allure.story("Login")
    @allure.title("Logging in with a valid, previously-registered account succeeds")
    @allure.severity(allure.severity_level.BLOCKER)
    def test_login_with_valid_credentials(self, page, ui_tester_url, registered_user):
        tester_page = TesterUrlPage(page)
        with allure.step("Go to the login page"):
            tester_page.navigate_to_login(ui_tester_url)

        with allure.step("Log in with the account created via API setup"):
            tester_page.login(
                registered_user["email"],
                registered_user["password"]
            )

        with allure.step("Successful login and the contact list display"):
            tester_page.wait_for_contact_list()
            assert "contactList" in page.url

    @allure.story("Login")
    @allure.title("Logging in with invalid credentials shows an error and stays on the login page")
    @allure.severity(allure.severity_level.NORMAL)
    def test_login_with_invalid_credentials_shows_error(self, page, ui_tester_url):
        tester_page = TesterUrlPage(page)
        with allure.step("Go to the login page and enter invalid credentials"):
            tester_page.navigate_to_login(ui_tester_url)
            tester_page.login(
                "invaliduser@example.com",
                "abcefddbb"
            )

        with allure.step("Assert an error is shown and the user is still on the login page"):
            error = tester_page.get_error_message()
            error.wait_for(state="visible")
            allure.attach(error.inner_text(), name="Error text", attachment_type=allure.attachment_type.TEXT)
            assert error.is_visible()
            assert "contactList" not in page.url


@allure.feature("Contact List UI")
class TestContacts:
    @allure.story("Add Contact")
    @allure.title("Adding a new contact makes it appear in the contact list")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_add_new_contact(self, page, ui_tester_url, registered_user, new_contact):
        tester_page = TesterUrlPage(page)
        with allure.step("Log in with a registered account"):
            tester_page.navigate_to_login(ui_tester_url)
            tester_page.login(
                registered_user["email"],
                registered_user["password"]
            )
            tester_page.wait_for_contact_list()

        with allure.step("Open the add-contact form and fill it in"):
            tester_page.open_add_contact()
            tester_page.add_contact(
                new_contact["firstName"],
                new_contact["lastName"],
                new_contact["email"],
                new_contact["phone"]
            )

        with allure.step("Assert the new contact appears in the contact list"):
            full_name = (
                f"{new_contact['firstName']} "
                f"{new_contact['lastName']}"
            )
            tester_page.verify_contact_visible(full_name)


@allure.feature("Contact List UI")
class TestEditContact:
    @allure.story("Edit Contact")
    @allure.title("Editing an existing contact updates its details in the contact list")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_edit_existing_contact(self, page, ui_tester_url, registered_user, new_contact):
        tester_page = TesterUrlPage(page)
        with allure.step("Log in with a registered account"):
            tester_page.navigate_to_login(ui_tester_url)
            tester_page.login(
                registered_user["email"],
                registered_user["password"]
            )
            tester_page.wait_for_contact_list()

        with allure.step("Add a contact to edit"):
            tester_page.open_add_contact()
            tester_page.add_contact(
                new_contact["firstName"],
                new_contact["lastName"],
                new_contact["email"],
                new_contact["phone"]
            )

        with allure.step("Open the contact and edit its last name"):
            full_name = (
                f"{new_contact['firstName']} "
                f"{new_contact['lastName']}"
            )
            tester_page.open_contact(full_name)
            tester_page.open_edit_contact()
            updated_last_name = "UpdatedLastName"
            tester_page.edit_contact(
                new_contact["firstName"],
                updated_last_name
            )

        with allure.step("Assert the updated name appears in the contact list"):
            tester_page.return_to_contact_list()
            updated_full_name = (
                f"{new_contact['firstName']} "
                f"{updated_last_name}"
            )
            allure.attach(updated_full_name, name="Expected updated name", attachment_type=allure.attachment_type.TEXT)
            tester_page.verify_contact_visible(updated_full_name)


@allure.feature("Contact List UI")
class TestDeleteContact:
    @allure.story("Delete Contact")
    @allure.title("Deleting a contact removes it from the contact list")
    @allure.severity(allure.severity_level.NORMAL)
    def test_delete_contact(self, page, ui_tester_url, registered_user, new_contact):
        tester_page = TesterUrlPage(page)
        with allure.step("Log in with a registered account"):
            tester_page.navigate_to_login(ui_tester_url)
            tester_page.login(
                registered_user["email"],
                registered_user["password"]
            )
            tester_page.wait_for_contact_list()

        with allure.step("Add a contact to delete"):
            tester_page.open_add_contact()
            tester_page.add_contact(
                new_contact["firstName"],
                new_contact["lastName"],
                new_contact["email"],
                new_contact["phone"]
            )

        full_name = f"{new_contact['firstName']} {new_contact['lastName']}"

        with allure.step("Open the contact and delete it"):
            tester_page.open_contact(full_name)
            tester_page.delete_contact()

        with allure.step("Assert the contact no longer appears in the contact list"):
            tester_page.verify_contact_not_visible(full_name)

@allure.feature("Contact List UI")
class TestLogout:
    @allure.story("Logout")
    @allure.title("Logging out returns the user to the login page")
    @allure.severity(allure.severity_level.NORMAL)
    def test_logout_returns_to_login_page(self, page, ui_tester_url, registered_user):
        tester_page = TesterUrlPage(page)
        with allure.step("Log in with a registered account"):
            tester_page.navigate_to_login(ui_tester_url)
            tester_page.login(
                registered_user["email"],
                registered_user["password"]
            )
            tester_page.wait_for_contact_list()

        with allure.step("Click Logout"):
            tester_page.logout()
        with allure.step("Assert the user is back on the login page"):
            page.wait_for_url(f"{ui_tester_url}/")
            assert tester_page.is_login_page_displayed()
            assert "contactList" not in page.url