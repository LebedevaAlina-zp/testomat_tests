from playwright.sync_api import Page, expect


class HomePage:
    def __init__(self, page: Page):
        self.page = page

    def open(self):
        self.page.goto("https://testomat.io")

    def is_loaded(self):
        expect(self.page.locator("#headerMenuWrapper")).to_be_visible()
        expect(self.page.locator(".side-menu .start-item")).to_be_visible()
        expect(self.page.locator(".side-menu .login-item")).to_be_visible()

    def click_login_button(self):
        self.page.locator(".side-menu .login-item").click()
