from enum import Enum
from typing import Self

from playwright.sync_api import Page, expect

from src.web.components.header import Header
from src.web.pages.base_page import BasePage


class NewProjectPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)

        self.header = Header(page)

        self.project_type_classical = self.root.locator("#classical")
        self.project_type_bdd = self.root.locator("#bdd")
        self.project_title_input = self.root.locator("#project_title")
        self.fill_demo_checkbox = self.root.locator("#demo-btn")

        self.create_project_button = self.root.locator("#project-create-btn input")

    def open(self) -> Self:
        self.page.goto("/projects/new")
        return self

    def is_loaded(self) -> Self:
        expect(self.header.dashboard_link).to_be_visible()
        expect(self.header.create_project_button).to_be_visible()
        expect(self.root.locator("h2")).to_have_text("New Project")
        expect(self.root.get_by_text("How to start?")).to_be_visible()
        expect(self.project_type_classical).to_contain_text("Classical")
        expect(self.project_type_bdd).to_contain_text("BDD")
        expect(self.project_title_input).to_be_visible()
        expect(self.create_project_button).to_be_visible()
        return self

    def create_new_project(self, project_title: str, project_type: ProjectType,
                           fill_demo: bool = False) -> Self:
        if project_type == ProjectType.CLASSICAL:
            self.project_type_classical.click()
        elif project_type == ProjectType.BDD:
            self.project_type_bdd.click()

        self.project_title_input.fill(project_title)

        if fill_demo:
            self.fill_demo_checkbox.check()

        self.create_project_button.click()
        expect(self.create_project_button).to_be_hidden(timeout=10_000)

        return self


class ProjectType(Enum):
    CLASSICAL = "classical"
    BDD = "bdd"
