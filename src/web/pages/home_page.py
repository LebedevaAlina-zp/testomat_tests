from typing import Self

from playwright.sync_api import Page, expect


class HomePage:
    def __init__(self, page: Page):
        self.page = page

    def open(self) -> Self:
        self.page.goto("https://testomat.io")
        return self

    def is_loaded(self):
        expect(self.page.locator("#headerMenuWrapper")).to_be_visible()
        expect(self.page.locator(".side-menu .start-item")).to_be_visible()
        expect(self.page.locator(".side-menu .login-item")).to_be_visible()
        return self

    def click_login_button(self):
        self.page.locator(".side-menu .login-item").click()
        return self
