import re
from typing import Self

from playwright.sync_api import Page, expect

from src.web.components import SideBarNav


class ProjectPage:
    def __init__(self, page: Page):
        self.page = page

        self.side_bar = SideBarNav(page)

        self.project_title = self.page.locator(".first h2")

        self.readme_block_resizer = self.page.locator(".resizer")
        self.readme_block_edit_btn = self.page.locator(".detail-view-actions [href*=readme]")
        self.readme_block_lets_start_btn = self.page.locator(".detail-view-content .primary-btn")
        self.readme_block_close_btn = self.page.locator(".back")

        self.input_new_suite_title = self.page.locator("[placeholder='First Suite']")
        self.add_suite_btn = self.page.get_by_role("button", name="Suite")

    def open_by_project_name(self, project_name: str) -> Self:
        """Acceptable project_name:
        project title (e.g. "Grocery & Shoes")
        or slug (e.g. "grocery-shoes")"""
        slug = re.sub(r"[^a-zA-Z0-9]+", "-", project_name)
        self.page.goto(f"/projects/{slug}")
        return self

    def open_by_id(self, project_id: str) -> Self:
        self.page.goto(f"/projects/{project_id}")
        return self

    def is_loaded(self) -> Self:
        expect(self.project_title).to_be_visible(timeout=20_000)
        expect(self.page.locator(".mainnav-menu")).to_be_visible(timeout=10_000)
        expect(self.page.locator("#welcometotestomatio")).to_be_visible()
        expect(self.readme_block_resizer).to_be_visible()
        expect(self.readme_block_edit_btn).to_be_visible()
        expect(self.readme_block_close_btn).to_be_visible()
        expect(self.input_new_suite_title).to_be_visible()
        expect(self.add_suite_btn).to_be_visible()
        return self

    def verify_project_title_is(self, expected_title) -> Self:
        expect(self.project_title).to_have_text(expected_title)
        return self

    def create_suite(self, suite_title: str) -> Self:
        """Create a test suite via '+ Test' dropdown menu"""
        self.page.get_by_role("button", name="Test").locator(
            ":scope + .ember-basic-dropdown button.btn-split-left"
        ).click()
        self.page.get_by_role("button", name="Suite", exact=False).click()
        self.page.get_by_role("combobox", name="Title").fill(suite_title)
        self.page.get_by_role("button", name="Save").fill(suite_title)
        return self

    def suite_with_title_is_visible(self, suite_title: str) -> Self:
        expect(self.page.locator(".suites-list-content").get_by_text(suite_title)).to_be_visible()
        return self
