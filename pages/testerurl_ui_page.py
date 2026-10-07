from playwright.sync_api import Page, expect


class TesterUrlPage:

    def __init__(self, page: Page):
        self.page = page

        # Login page
        self.email_input = page.get_by_role(
            "textbox", name="Email"
        )
        self.password_input = page.get_by_role(
            "textbox", name="Password"
        )
        self.submit_button = page.get_by_role(
            "button", name="Submit"
        )
        self.signup_button = page.get_by_role(
            "button", name="Sign up"
        )
        self.error_message = page.locator("#error")

        # Contact list
        self.add_contact_button = page.get_by_role(
            "button", name="Add a New Contact"
        )
        self.edit_contact_button = page.get_by_role(
            "button", name="Edit Contact"
        )
        self.delete_contact_button = page.get_by_role(
            "button", name="Delete Contact"
        )
        self.return_to_contact_list_button = page.get_by_role(
            "button", name="Return to Contact List"
        )
        self.logout_button = page.get_by_role(
            "button", name="Logout"
        )

    # -------------------------
    # Navigation
    # -------------------------

    def navigate_to_login(self, base_url):
        self.page.goto(f"{base_url}/")

    def wait_for_contact_list(self):
        self.page.wait_for_url("**/contactList")

    # -------------------------
    # Login
    # -------------------------

    def login(self, email, password):
        self.email_input.fill(email)
        self.password_input.fill(password)
        self.submit_button.click()

    def is_login_page_displayed(self):
        return self.submit_button.is_visible()

    def get_error_message(self):
        return self.error_message

    # -------------------------
    # Sign Up
    # -------------------------

    def open_signup(self):
        self.signup_button.click()

    def signup(self, first_name, last_name, email, password):
        self.page.get_by_role(
            "textbox", name="First Name"
        ).fill(first_name)

        self.page.get_by_role(
            "textbox", name="Last Name"
        ).fill(last_name)

        self.page.get_by_role(
            "textbox", name="Email"
        ).fill(email)

        self.page.get_by_role(
            "textbox", name="Password"
        ).fill(password)

        self.page.get_by_role(
            "button", name="Submit"
        ).click()

    # -------------------------
    # Add Contact
    # -------------------------

    def open_add_contact(self):
        self.add_contact_button.click()

    def add_contact(
        self,
        first_name,
        last_name,
        email,
        phone
    ):
        self.page.get_by_role(
            "textbox", name="First Name:"
        ).fill(first_name)

        self.page.get_by_role(
            "textbox", name="Last Name:"
        ).fill(last_name)

        self.page.get_by_role(
            "textbox", name="Email:"
        ).fill(email)

        self.page.get_by_role(
            "textbox", name="Phone:"
        ).fill(phone)

        self.page.get_by_role(
            "button", name="Submit"
        ).click()

        self.wait_for_contact_list()

    # -------------------------
    # Contact
    # -------------------------

    def open_contact(self, full_name):
        self.page.get_by_text(
            full_name,
            exact=True
        ).click()

    def verify_contact_visible(self, full_name):
        expect(
            self.page.get_by_text(
                full_name,
                exact=True
            )
        ).to_be_visible()

    def verify_contact_not_visible(self, full_name):
        expect(
            self.page.get_by_text(
                full_name,
                exact=True
            )
        ).not_to_be_visible()

    # -------------------------
    # Edit Contact
    # -------------------------

    def open_edit_contact(self):
        self.edit_contact_button.click()

    def edit_contact(
        self,
        first_name,
        updated_last_name
    ):
        first_name_field = self.page.get_by_role(
            "textbox",
            name="First Name:"
        )

        expect(first_name_field).to_have_value(
            first_name
        )

        first_name_field.fill(first_name)

        self.page.get_by_role(
            "textbox",
            name="Last Name:"
        ).fill(updated_last_name)

        self.page.get_by_role(
            "button", name="Submit"
        ).click()

    def return_to_contact_list(self):
        self.return_to_contact_list_button.click()
        self.wait_for_contact_list()

    # -------------------------
    # Delete Contact
    # -------------------------

    def delete_contact(self):
        self.page.once(
            "dialog",
            lambda dialog: dialog.accept()
        )

        self.delete_contact_button.click()

        self.wait_for_contact_list()

    # -------------------------
    # Logout
    # -------------------------

    def logout(self):
        self.logout_button.click()