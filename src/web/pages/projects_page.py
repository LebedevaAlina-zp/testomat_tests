from playwright.sync_api import Page, expect

from src.web.components.header import Header
from src.web.components.project_card import ProjectCard
from src.web.pages.base_page import BasePage


class ProjectsPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)

        self.header = Header(page)

        self.sign_in_flash_message = self.root.locator(".common-flash-success", has_text="Signed in successfully")

        self.projects_header = self.root.locator(".common-page-header")
        self.search_input = self.root.locator("#search")

        self.grid = self.root.locator("#grid")
        self.project_cards = self.grid.locator("li")

    def open(self):
        self.page.goto("/")

    def is_loaded(self):
        expect(self.header.dashboard_link).to_be_visible()
        expect(self.header.create_project_button).to_be_visible()
        expect(self.search_input).to_be_visible()
        expect(self.grid).to_be_visible()

    def search_project(self, name: str):
        self.search_input.fill(name, force=True)

    def get_projects(self) -> list[ProjectCard]:
        return [
            ProjectCard(card)
            for card in self.project_cards.all()
        ]

    def open_project_by_name(self, name: str):
        card = self.project_cards.filter(has_text=name).first
        ProjectCard(card).open()
