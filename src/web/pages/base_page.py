from playwright.sync_api import Page, Locator


class BasePage:
    def __init__(self, page: Page):
        self.page = page
        # Root for DESKTOP
        self.root: Locator = page.locator("#content-desktop")
