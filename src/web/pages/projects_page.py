from playwright.sync_api import Page, expect


class ProjectsPage:
    def __init__(self, page: Page):
        self.page = page

    def open(self):
        self.page.goto("/")

    def is_loaded(self):
        expect(self.page.locator(".common-flash-success", has_text="Signed in successfully")).to_be_visible()
