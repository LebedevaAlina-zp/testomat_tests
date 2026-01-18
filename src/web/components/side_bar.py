from playwright.sync_api import Locator, Page


class SideBar():
    def __init__(self, page: Page):
        self.page = page
        self._menu_container = page.locator(".mainnav-menu")

    @property
    def toggle_button(self) -> Locator:
        return self._menu_container.get_by_role("button")

    @property
    def tests_link(self) -> Locator:
        return self._menu_container.get_by_role("link", name="Tests")

    @property
    def requirements_link(self) -> Locator:
        return self._menu_container.get_by_role("link", name="Requirements")

    @property
    def runs_link(self) -> Locator:
        return self._menu_container.get_by_role("link", name="Runs")

    @property
    def plans_link(self) -> Locator:
        return self._menu_container.get_by_role("link", name="Plans")

    @property
    def steps_link(self) -> Locator:
        return self._menu_container.get_by_role("link", name="Steps")

    @property
    def pulse_link(self) -> Locator:
        return self._menu_container.get_by_role("link", name="Pulse")

    @property
    def imports_link(self) -> Locator:
        return self._menu_container.get_by_role("link", name="Imports")

    @property
    def analytics_link(self) -> Locator:
        return self._menu_container.get_by_role("link", name="Analytics")

    @property
    def branches_link(self) -> Locator:
        return self._menu_container.get_by_role("link", name="Branches")

    @property
    def settings_link(self) -> Locator:
        return self._menu_container.get_by_role("link", name="Settings")

    @property
    def help_link(self) -> Locator:
        return self._menu_container.get_by_role("link", name="Help")

    @property
    def projects_link(self) -> Locator:
        return self._menu_container.get_by_role("link", name="Projects")

    @property
    def profile_link(self) -> Locator:
        return self._menu_container.get_by_role("link", name="Profile")
