from playwright.sync_api import Page, expect

from src.web.pages.base_page import BasePage


class LoginPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)

    def open(self):
        self.page.goto("/users/sign_in")

    def is_loaded(self):
        expect(self.page.locator(".side-menu .login-item")).to_be_visible()

    def login(self, email: str, password: str):
        self.root.locator("#user_email").fill(email)
        self.root.locator("#user_password").fill(password)
        self.page.get_by_role("button", name="Sign In").click()

    def invalid_login_message_visible(self):
        expect(self.root.get_by_text("Invalid Email or password.")).to_be_visible()
