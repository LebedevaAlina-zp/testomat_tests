import re
from typing import Self

from playwright.sync_api import Page, expect


class SideBarNav:
    def __init__(self, page: Page):
        self.page = page
        self._menu_container = page.locator(".mainnav-menu")

        self.toggle_button = self._menu_container.get_by_role("button")
        self.tests_link = self._menu_container.get_by_role("link", name="Tests")
        self.requirements_link = self._menu_container.get_by_role("link", name="Requirements")
        self.runs_link = self._menu_container.get_by_role("link", name="Runs")
        self.plans_link = self._menu_container.get_by_role("link", name="Plans")
        self.steps_link = self._menu_container.get_by_role("link", name="Steps")
        self.pulse_link = self._menu_container.get_by_role("link", name="Pulse")
        self.imports_link = self._menu_container.get_by_role("link", name="Imports")
        self.analytics_link = self._menu_container.get_by_role("link", name="Analytics")
        self.branches_link = self._menu_container.get_by_role("link", name="Branches")
        self.settings_link = self._menu_container.get_by_role("link", name="Settings")
        self.help_link = self._menu_container.get_by_role("link", name="Help")
        self.projects_link = self._menu_container.get_by_role("link", name="Projects")
        self.profile_link = self._menu_container.get_by_role("link", name="Profile")

        self._links = {
            "Tests": self.tests_link,
            "Requirements": self.requirements_link,
            "Runs": self.runs_link,
            "Plans": self.plans_link,
            "Steps": self.steps_link,
            "Pulse": self.pulse_link,
            "Imports": self.imports_link,
            "Analytics": self.analytics_link,
            "Branches": self.branches_link,
            "Settings": self.settings_link,
            "Help": self.help_link,
            "Projects": self.projects_link,
            "Profile": self.profile_link,
        }

    def is_loaded(self) -> Self:
        expect(self._menu_container).to_be_visible()
        expect(self.toggle_button).to_be_visible()
        return self

    def expect_tab_active(self, name: str):
        expect(self._links[name]).to_have_attribute("class", re.compile(r"\bactive\b"))
        return self

    def open_side_bar(self):
        self.toggle_button.click()
        return self

    def click_tests(self):
        self.tests_link.click()
        return self

    def click_requirements(self):
        self.requirements_link.click()
        return self

    def click_runs(self):
        self.runs_link.click()
        return self

    def click_plans(self):
        self.plans_link.click()
        return self

    def click_steps(self):
        self.steps_link.click()
        return self

    def click_pulse(self):
        self.pulse_link.click()
        return self

    def click_imports(self):
        self.imports_link.click()
        return self

    def click_analytics(self):
        self.analytics_link.click()
        return self

    def click_branches(self):
        self.branches_link.click()
        return self

    def click_settings(self):
        self.settings_link.click()
        return self

    def click_help(self):
        self.help_link.click()
        return self

    def click_projects(self):
        self.projects_link.click()
        return self

    def click_profile(self):
        self.profile_link.click()
        return self
