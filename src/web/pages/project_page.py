import re
from typing import Self

from playwright.sync_api import Page, expect

from src.web.components import (
    EmptyProjectTestsTab,
    ProjectPageTestsTab,
    SideBarNav,
    SuiteCreationForm,
)


class ProjectPage:
    def __init__(self, page: Page):
        self.page = page

        self.side_bar = SideBarNav(page)
        self.suite_creation_form = SuiteCreationForm(page)

        # Tests tab (default opened) differs depending on whether a project has suites
        self.tests_tab = ProjectPageTestsTab(page)
        self.empty_project_tests_tab = EmptyProjectTestsTab(page)

        self.current_tab_name = self.page.locator(".breadcrumbs-page-second-level")

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
        self.side_bar.is_loaded()
        expect(self.current_tab_name).to_have_text("Tests")
        self.tests_tab.is_loaded()
        return self

    def is_loaded_empty(self):
        self.side_bar.is_loaded()
        self.empty_project_tests_tab.is_loaded()
        self.empty_project_tests_tab.readme_block.is_loaded()
        return self

    def verify_project_title_is(self, expected_title) -> Self:
        expect(self.project_title).to_have_text(expected_title)
        return self

    def create_suite(self, suite_title: str) -> Self:
        """Create a test suite via '+ Suite' in '+ Test' dropdown menu"""
        self.page.get_by_role("button", name="Test").locator(
            ":scope + .ember-basic-dropdown button.btn-split-left"
        ).click()
        self.page.get_by_text("Collection of test cases").click()
        self.suite_creation_form.is_loaded()
        self.suite_creation_form.fill_suite_form(suite_title)
        self.suite_creation_form.save_suite()
        return self

    def suite_with_title_is_visible(self, suite_title: str) -> Self:
        expect(
            self.page.locator(".suites-list-content").get_by_text(suite_title)
        ).to_be_visible()
        return self
