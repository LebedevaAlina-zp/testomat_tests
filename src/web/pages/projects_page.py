from dataclasses import dataclass
from typing import Self

from playwright.sync_api import Page, expect

from src.web.components.header_nav import HeaderNav
from src.web.components.project_card import ProjectCard


class ProjectsPage:
    def __init__(self, page: Page):
        self.page = page
        self._root = self.page.locator("#content-desktop")

        self.header = HeaderNav(page)

        self.sign_in_flash_message = self._root.locator(".common-flash-success", has_text="Signed in successfully")

        # Page header (Projects header area)
        self.page_header = self._root.locator(".common-page-header")

        # Projects header elements
        self.company_dropdown = self.page_header.locator("#company_id")
        self.current_subscription = self.page_header.locator(".tooltip-project-plan span")
        self.create_company_btn = self.page_header.get_by_role("link", name="Create Company to Upgrade")
        self.view_switcher = self.page_header.locator(".common-page-header-icons")
        self.grid_view_icon = self.view_switcher.locator("svg[data-icon='grid']")
        self.table_view_icon = self.view_switcher.locator("svg[data-icon='table']")

        self.search_input = self._root.locator("#search")

        self.grid = self._root.locator("#grid")
        self.project_cards = self.grid.locator("li")

    def open(self) -> Self:
        self.page.goto("/")
        return self

    def is_loaded(self) -> Self:
        expect(self.header.dashboard_link).to_be_visible()
        expect(self.header.create_project_button).to_be_visible()
        expect(self.search_input).to_be_visible()
        expect(self.grid).to_be_visible()
        return self

    def search_project(self, name: str) -> Self:
        self.search_input.fill(name, force=True)
        return self

    def get_projects(self) -> list[ProjectCard]:
        return [
            ProjectCard(card)
            for card in self.project_cards.all()
        ]

    def open_project_by_name(self, name: str) -> Self:
        card = self.project_cards.filter(has_text=name).first
        ProjectCard(card).open()
        return self

    @property
    def company_options(self) -> CompanyOptions:
        return CompanyOptions(
            qa_club_lviv="789",
            free_projects=""
        )

    def select_company(self, company: CompanyOptions):
        self.company_dropdown.click()
        self.company_dropdown.select_option(company)
        return self


@dataclass
class CompanyOptions:
    qa_club_lviv: str
    free_projects: str
