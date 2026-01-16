from playwright.sync_api import Locator, Page

from src.web.components.base_component import BaseComponent
from src.web.components.profile_menu import ProfileMenu


# from src.web.components.global_search import GlobalSearch

class Header(BaseComponent):
    def __init__(self, page: Page):
        super().__init__(page)
        self.container: Locator = self.root.locator(".auth-header-nav")

    @property
    def dashboard_link(self) -> Locator:
        return self.container.locator(".auth-header-nav-left-items a[href='/']")

    @property
    def companies_link(self) -> Locator:
        return self.container.locator("a[href='/companies']")

    @property
    def create_project_button(self) -> Locator:
        return self.container.locator("a[href='/projects/new']")

    # @property
    # def global_search_button(self) -> Locator:
    #     return self.container.locator("#showGlobalSearchBtn")

    @property
    def profile_avatar(self) -> Locator:
        return self.container.locator("#toggle-profile-menu")

    # def open_global_search(self) -> GlobalSearch:
    #     self.global_search_button.click()
    #     return GlobalSearch(self.page)

    def open_profile_menu(self) -> ProfileMenu:
        self.profile_avatar.click()
        return ProfileMenu(self.page)
