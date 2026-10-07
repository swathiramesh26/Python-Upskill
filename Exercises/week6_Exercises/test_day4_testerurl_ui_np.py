"""
UI tests for https://thinking-tester-contact-list.herokuapp.com
5 UI tests - Allure annotations and CI pipelines
"""

import allure
from playwright.sync_api import expect

@allure.feature("Contact List UI")
class TestSignup:
    @allure.story("Sign Up")
    @allure.title("Signing up with a new email creates an account and shows the contact list")
    @allure.severity(allure.severity_level.BLOCKER)
    def test_signup_creates_account(self, page, ui_tester_url, new_user):
        with allure.step("Go to the app and open the sign up form"):
            page.goto(f"{ui_tester_url}/")
            page.get_by_role("button", name="Sign up").click()

        with allure.step("Fill in the sign up form with unique user"):
            page.get_by_role("textbox", name="First Name").fill(new_user["firstName"])
            page.get_by_role("textbox", name="Last Name").fill(new_user["lastName"])
            page.get_by_role("textbox", name="Email").fill(new_user["email"])
            page.get_by_role("textbox", name="Password").fill(new_user["password"])
            page.get_by_role("button", name="Submit").click()

        with allure.step("Assert the account was created and the contact list is shown"):
            page.wait_for_url("**/contactList")
            allure.attach(page.url, name="Landed on URL", attachment_type=allure.attachment_type.TEXT)
            assert "contactList" in page.url


@allure.feature("Contact List UI")
class TestLogin:
    @allure.story("Login")
    @allure.title("Logging in with a valid, previously-registered account succeeds")
    @allure.severity(allure.severity_level.BLOCKER)
    def test_login_with_valid_credentials(self, page, ui_tester_url, registered_user):
        with allure.step("Go to the login page"):
            page.goto(f"{ui_tester_url}/")

        with allure.step("Log in with the account created via API setup"):
            page.get_by_role("textbox", name="Email").fill(registered_user["email"])
            page.get_by_role("textbox", name="Password").fill(registered_user["password"])
            page.get_by_role("button", name="Submit").click()

        with allure.step("Successful login and the contact list display"):
            page.wait_for_url("**/contactList")
            assert "contactList" in page.url

    @allure.story("Login")
    @allure.title("Logging in with invalid credentials shows an error and stays on the login page")
    @allure.severity(allure.severity_level.NORMAL)
    def test_login_with_invalid_credentials_shows_error(self, page, ui_tester_url):
        with allure.step("Go to the login page and enter invalid credentials"):
            page.goto(f"{ui_tester_url}/")
            page.get_by_role("textbox", name="Email").fill("invaliduser@example.com")
            page.get_by_role("textbox", name="Password").fill("abcefddbb")
            page.get_by_role("button", name="Submit").click()

        with allure.step("Assert an error is shown and the user is still on the login page"):
            error = page.locator("#error")
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
        with allure.step("Log in with a registered account"):
            page.goto(f"{ui_tester_url}/")
            page.get_by_role("textbox", name="Email").fill(registered_user["email"])
            page.get_by_role("textbox", name="Password").fill(registered_user["password"])
            page.get_by_role("button", name="Submit").click()
            page.wait_for_url("**/contactList")

        with allure.step("Open the add-contact form and fill it in"):
            page.get_by_role("button", name="Add a New Contact").click()
            page.get_by_role("textbox", name="First Name:").fill(new_contact["firstName"])
            page.get_by_role("textbox", name="Last Name:").fill(new_contact["lastName"])
            page.get_by_role("textbox", name="Email:").fill(new_contact["email"])
            page.get_by_role("textbox", name="Phone:").fill(new_contact["phone"])
            page.get_by_role("button", name="Submit").click()
            page.wait_for_url("**/contactList")

        with allure.step("Assert the new contact appears in the contact list"):
            page.wait_for_url("**/contactList")
            full_name = f"{new_contact['firstName']} {new_contact['lastName']}"
            # assert page.get_by_text(full_name).is_visible()-- throws error for chrome
            expect(self.page.get_by_text(full_name)).to_be_visible()


@allure.feature("Contact List UI")
class TestEditContact:
    @allure.story("Edit Contact")
    @allure.title("Editing an existing contact updates its details in the contact list")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_edit_existing_contact(self, page, ui_tester_url, registered_user, new_contact):
        with allure.step("Log in with a registered account"):
            page.goto(f"{ui_tester_url}/")
            page.get_by_role("textbox", name="Email").fill(registered_user["email"])
            page.get_by_role("textbox", name="Password").fill(registered_user["password"])
            page.get_by_role("button", name="Submit").click()
            page.wait_for_url("**/contactList")

        with allure.step("Add a contact to edit"):
            page.get_by_role("button", name="Add a New Contact").click()
            page.get_by_role("textbox", name="First Name:").fill(new_contact["firstName"])
            page.get_by_role("textbox", name="Last Name:").fill(new_contact["lastName"])
            page.get_by_role("textbox", name="Email:").fill(new_contact["email"])
            page.get_by_role("textbox", name="Phone:").fill(new_contact["phone"])
            page.get_by_role("button", name="Submit").click()
            page.wait_for_url("**/contactList")

        with allure.step("Open the contact and edit its last name"):
            full_name = f"{new_contact['firstName']} {new_contact['lastName']}"
            page.get_by_text(full_name, exact=True).click()
            page.get_by_role("button", name="Edit Contact").click()
            updated_last_name = "UpdatedLastName"
            first_name_field = page.get_by_role("textbox", name="First Name:")
            expect(first_name_field).to_have_value(new_contact["firstName"])
            first_name_field.fill(new_contact["firstName"])
            page.get_by_role("textbox", name="Last Name:").fill(updated_last_name)
            page.get_by_role("button", name="Submit").click()

        with allure.step("Assert the updated name appears in the contact list"):
            page.get_by_role("button", name="Return to Contact List").click()
            page.wait_for_url("**/contactList")
            updated_full_name = f"{new_contact['firstName']} {updated_last_name}"
            allure.attach(updated_full_name, name="Expected updated name", attachment_type=allure.attachment_type.TEXT)
            expect(page.get_by_text(updated_full_name)).to_be_visible()


@allure.feature("Contact List UI")
class TestDeleteContact:
    @allure.story("Delete Contact")
    @allure.title("Deleting a contact removes it from the contact list")
    @allure.severity(allure.severity_level.NORMAL)
    def test_delete_contact(self, page, ui_tester_url, registered_user, new_contact):
        with allure.step("Log in with a registered account"):
            page.goto(f"{ui_tester_url}/")
            page.get_by_role("textbox", name="Email").fill(registered_user["email"])
            page.get_by_role("textbox", name="Password").fill(registered_user["password"])
            page.get_by_role("button", name="Submit").click()
            page.wait_for_url("**/contactList")

        with allure.step("Add a contact to delete"):
            page.get_by_role("button", name="Add a New Contact").click()
            page.get_by_role("textbox", name="First Name:").fill(new_contact["firstName"])
            page.get_by_role("textbox", name="Last Name:").fill(new_contact["lastName"])
            page.get_by_role("textbox", name="Email:").fill(new_contact["email"])
            page.get_by_role("textbox", name="Phone:").fill(new_contact["phone"])
            page.get_by_role("button", name="Submit").click()
            page.wait_for_url("**/contactList")

        full_name = f"{new_contact['firstName']} {new_contact['lastName']}"

        with allure.step("Open the contact and delete it"):
            page.get_by_text(full_name).click()
            page.once("dialog", lambda dialog: dialog.accept()) # To click OK when dialog box shows up
            page.get_by_role("button", name="Delete Contact").click()

        with allure.step("Assert the contact no longer appears in the contact list"):
            page.wait_for_url("**/contactList")
            expect(page.get_by_text(full_name)).not_to_be_visible()

@allure.feature("Contact List UI")
class TestLogout:
    @allure.story("Logout")
    @allure.title("Logging out returns the user to the login page")
    @allure.severity(allure.severity_level.NORMAL)
    def test_logout_returns_to_login_page(self, page, ui_tester_url, registered_user):
        with allure.step("Log in with a registered account"):
            page.goto(f"{ui_tester_url}/")
            page.get_by_role("textbox", name= "Email").fill(registered_user["email"])
            page.get_by_role("textbox", name="Password").fill(registered_user["password"])
            page.get_by_role("button", name="Submit").click()
            page.wait_for_url("**/contactList")

        with allure.step("Click Logout"):
            page.get_by_role("button", name="Logout").click()
        with allure.step("Assert the user is back on the login page"):
            page.wait_for_url(f"{ui_tester_url}/")
            assert page.get_by_role("button", name="Submit").is_visible()
            assert "contactList" not in page.url