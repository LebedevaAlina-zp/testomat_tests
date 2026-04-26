from typing import Self

import allure
from playwright.sync_api import Page, expect


class SuiteCreationForm:
    def __init__(self, page: Page):
        self.page = page
        self.form_heading = self.page.get_by_role("heading", name="New Suite")
        self.title_textbox = self.page.get_by_role("combobox", name="Title")
        self.save_btn = self.page.get_by_role("button", name="Save")
        self.cancel_btn = self.page.get_by_role("link", name="Cancel")
        self.close_form_icon = self.page.locator(".back")

    @allure.step("Verify suite creation form is loaded")
    def is_loaded(self) -> Self:
        expect(self.form_heading).to_be_visible()
        expect(self.title_textbox).to_be_visible()
        expect(self.save_btn).to_be_visible()
        expect(self.cancel_btn).to_be_visible()
        expect(self.close_form_icon).to_be_visible()
        return self

    @allure.step("Fill the suite create form")
    def fill_suite_form(self, title: str) -> Self:
        self.title_textbox.fill(title)
        return self

    @allure.step("Click 'Save' button")
    def save_suite(self) -> Self:
        self.save_btn.click()
        return self

    @allure.step("Click 'Cancel' button")
    def cancel_suite_creation(self) -> None:
        self.cancel_btn.click()

    @allure.step("Close the suite creation form")
    def close_panel(self) -> None:
        self.close_form_icon.click()
