from typing import Self

from playwright.sync_api import Locator, Page, expect


class HeaderNav:
    def __init__(self, page: Page):
        self.page = page
        self._header_container = self.page.locator("#content-desktop .auth-header-nav")

    @property
    def dashboard(self) -> Locator:
        return self._header_container.locator(".auth-header-nav-left-items a[href='/']")

    @property
    def companies(self) -> Locator:
        return self._header_container.get_by_role("link", name="Companies")

    @property
    def create_project_icon(self) -> Locator:
        return self._header_container.locator("a[href='/projects/new']")

    @property
    def profile_avatar(self) -> Locator:
        return self._header_container.locator("#toggle-profile-menu")

    # @property
    # def global_search_icon(self) -> Locator:
    #     return self.container.locator("#showGlobalSearchBtn")

    # def open_profile_menu(self) -> ProfileMenu:
    #     self.profile_avatar.click()
    #     return ProfileMenu(self.page)

    def is_loaded(self) -> Self:
        expect(self.dashboard).to_be_visible()
        expect(self.companies).to_be_visible()
        expect(self.create_project_icon).to_be_visible()
        expect(self.profile_avatar).to_be_visible()
        return self
