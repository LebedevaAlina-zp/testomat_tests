from typing import Self

import allure
from playwright.sync_api import Page, expect


class ProjectPageTestsTab:
    """Tests tab on project page: https://app.testomat.io/projects/{project_id}/"""

    def __init__(self, page: Page):
        self.page = page

        self.tab_name = self.page.locator(".breadcrumbs-page-second-level")
        self.filter_bar_icon = self.page.locator(".filterbar-filter-btn-div")
        self.search_textbox = self.page.locator("input[name='search']")
        self.add_test_btn = self.page.get_by_role("button", name="Test", exact=True)
        self.add_test_dropdown = self.page.locator(".md-icon-chevron-down")
        self.suites_box = self.page.locator(".suites-list-content")
        self.suite_item = self.page.locator(".node-link")

    @allure.step
    def is_loaded(self) -> Self:
        expect(self.tab_name).to_have_text("Tests")
        expect(self.filter_bar_icon).to_be_visible(timeout=20000)
        expect(self.search_textbox).to_be_visible()
        expect(self.add_test_btn).to_be_visible(timeout=20000)
        expect(self.add_test_dropdown).to_be_visible()
        expect(self.suites_box).to_be_visible()
        return self
