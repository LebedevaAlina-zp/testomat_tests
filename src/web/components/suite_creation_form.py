from typing import Self

from playwright.sync_api import Page, expect


class SuiteCreationForm:
    def __init__(self, page: Page):
        self.page = page
        self.form_heading = self.page.get_by_role("heading", name="New Suite")
        self.title_textbox = self.page.get_by_role("combobox", name="Title")
        self.save_btn = self.page.get_by_role("button", name="Save")
        self.cancel_btn = self.page.get_by_role("link", name="Cancel")
        self.close_form_icon = self.page.locator(".back")

    def is_loaded(self) -> Self:
        expect(self.form_heading).to_be_visible()
        expect(self.title_textbox).to_be_visible()
        expect(self.save_btn).to_be_visible()
        expect(self.cancel_btn).to_be_visible()
        expect(self.close_form_icon).to_be_visible()
        return self

    def fill_suite_form(self, title: str) -> Self:
        self.title_textbox.fill(title)
        return self

    def save_suite(self) -> Self:
        self.save_btn.click()
        return self

    def cancel_suite_creation(self) -> None:
        self.cancel_btn.click()

    def close_panel(self) -> None:
        self.close_form_icon.click()
