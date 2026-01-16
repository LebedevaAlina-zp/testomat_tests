from playwright.sync_api import Page, expect

from src.web.pages.base_page import BasePage


class LoginPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)

        self.signup_href = self.root.locator("a", has_text="Sign Up")

        self.auth_with_google = self.root.locator(".button-auth", has_text="Google")
        self.auth_with_github = self.root.locator(".button-auth", has_text="GitHub")
        self.auth_with_sso = self.root.locator(".button-auth", has_text="SSO")

        self.email_input = self.root.locator("#user_email")
        self.password_input = self.root.locator("#user_password")
        self.remember_me_checkbox = self.root.locator("#user_remember_me")
        self.signin_btn = page.get_by_role("button", name="Sign In")


    def open(self):
        self.page.goto("/users/sign_in")

    def is_loaded(self):
        expect(self.signup_href).to_be_visible(timeout=10000)
        expect(self.auth_with_google).to_be_visible
        expect(self.auth_with_github).to_be_visible()
        expect(self.auth_with_sso).to_be_visible()

        expect(self.email_input).to_be_visible()
        expect(self.password_input).to_be_visible()
        expect(self.remember_me_checkbox).to_be_visible()
        expect(self.signin_btn).to_be_visible()

    def login(self, email: str, password: str, remember_me: bool = False):
        self.email_input.fill(email)
        self.password_input.fill(password)

        if remember_me:
            self.remember_me_checkbox.check()

        self.signin_btn.click()

    def invalid_login_message_visible(self):
        expect(self.root.get_by_text("Invalid Email or password.")).to_be_visible()
