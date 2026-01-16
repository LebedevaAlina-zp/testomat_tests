from playwright.sync_api import Page, Locator


class BaseComponent:
    def __init__(self, page: Page, root: Locator | None = None):
        self.page = page
        # Root for DESKTOP
        self.root = root or page.locator("#content-desktop")
