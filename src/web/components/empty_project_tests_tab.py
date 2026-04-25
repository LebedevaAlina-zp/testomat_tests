from typing import Self

import allure
from playwright.sync_api import Page, expect

from src.web.components.project_page_readme_block import (
    ReadmeBlock,
)


class EmptyProjectTestsTab:
    def __init__(self, page: Page):
        self.page = page

        self.readme_block = ReadmeBlock(page)
        self.project_title = self.page.locator(".first h2")

        self.input_new_suite_title = self.page.locator("[placeholder='First Suite']")
        self.add_suite_btn = self.page.get_by_role("button", name="Suite")

    def is_loaded(self) -> Self:
        expect(self.project_title).to_be_visible()
        expect(self.input_new_suite_title).to_be_visible()
        expect(self.add_suite_btn).to_be_visible()
        return self

    @allure.step
    def verify_project_title_is(self, expected_title) -> Self:
        expect(self.project_title).to_have_text(expected_title)
        return self

    @allure.step
    def create_quickstart_suite(self, suite_title) -> Self:
        self.input_new_suite_title.fill(suite_title)
        self.add_suite_btn.click()
        return self
