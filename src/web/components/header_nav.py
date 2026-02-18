from playwright.sync_api import Locator, Page


class HeaderNav:
    def __init__(self, page: Page):
        self.page = page
        self._header_container = self.page.locator("#content-desktop .auth-header-nav")

    @property
    def dashboard_link(self) -> Locator:
        return self._header_container.locator(".auth-header-nav-left-items a[href='/']")

    @property
    def companies_link(self) -> Locator:
        return self._header_container.locator("a[href='/companies']")

    @property
    def create_project_button(self) -> Locator:
        return self._header_container.locator("a[href='/projects/new']")

    @property
    def profile_avatar(self) -> Locator:
        return self._header_container.locator("#toggle-profile-menu")

    # @property
    # def global_search_button(self) -> Locator:
    #     return self.container.locator("#showGlobalSearchBtn")

    # def open_profile_menu(self) -> ProfileMenu:
    #     self.profile_avatar.click()
    #     return ProfileMenu(self.page)
