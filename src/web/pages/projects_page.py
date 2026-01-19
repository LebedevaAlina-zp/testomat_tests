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
        self.company_selected = self.page_header.locator(".common-page-header-subtitle button")
        self.company_dropdown = self.page_header.locator(".common-page-header-subtitle .dropdown-menu")
        self.current_plan = self.page_header.locator(".common-page-header-title span")
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
    