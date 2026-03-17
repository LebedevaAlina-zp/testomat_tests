from dataclasses import dataclass
from typing import Self

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

from src.web.selenium.core.base_page import BasePage
from tests.fixtures.config import Config


@dataclass
class CompanyOptions:
    qa_club_lviv: str
    free_projects: str


class ProjectsPage(BasePage):
    # Projects header elements
    PAGE_TITLE = (By.CSS_SELECTOR, ".common-page-header h2")

    # Common elements
    COMPANY_DROPDOWN = (By.CSS_SELECTOR, "#content-desktop #company_id")
    CURRENT_PLAN = (By.CSS_SELECTOR, ".tooltip-project-plan span")
    GRID_ICON = (By.CSS_SELECTOR, "#grid-icon")
    TABLE_ICON = (By.CSS_SELECTOR, "#table-icon")
    SEARCH_INPUT = (By.CSS_SELECTOR, "#search")

    # Free plan elements
    CREATE_COMPANY_BTN = (By.CSS_SELECTOR, "[href='/companies/new']")
    HAVE_NOT_CREATED_PROJECTS_TEXT = (By.CSS_SELECTOR, ".items-center p")
    CREATE_PROJECT_CENTER_BTN = (By.CSS_SELECTOR, ".items-center .common-btn-lg[href]")

    # Enterprise plan elements
    PROJECT_CARDS = (By.CSS_SELECTOR, "#content-desktop li")

    def __init__(self, driver: WebDriver, configs: Config):
        super().__init__(driver, configs)

    def open(self):
        self.driver.get(self.configs.base_app_url)
        return self

    def _header_is_loaded(self):
        self.wait.for_visible(self.PAGE_TITLE)
        assert self.get_text(self.PAGE_TITLE) == "Projects"
        self.wait.for_visible(self.COMPANY_DROPDOWN)
        self.wait.for_visible(self.CURRENT_PLAN)
        self.wait.for_visible(self.GRID_ICON)
        self.wait.for_visible(self.TABLE_ICON)
        self.wait.for_visible(self.SEARCH_INPUT)

    def is_loaded_free_plan(self):
        self._header_is_loaded()
        self.wait.for_visible(self.CREATE_COMPANY_BTN)
        assert self.find(self.CURRENT_PLAN).text == "Free Plan"
        self.wait.for_visible(self.CREATE_PROJECT_CENTER_BTN)
        assert (
            self.find(self.HAVE_NOT_CREATED_PROJECTS_TEXT).text
            == "You have not created any projects yet"
        )

    def is_loaded_default_enterprise(self):
        self._header_is_loaded()
        assert self.find(self.CURRENT_PLAN).text == "Enterprise Plan"
        self.wait.for_visible(self.PROJECT_CARDS)

    @property
    def company_options(self) -> CompanyOptions:
        return CompanyOptions(qa_club_lviv="789", free_projects="")

    def click_company_dropdown(self) -> Self:
        self.driver.find_element(*self.COMPANY_DROPDOWN).click()
        return self

    def choose_company_in_dropdown_list(self, company: CompanyOptions) -> Self:
        self.wait.for_visible(self.COMPANY_DROPDOWN)
        self.driver.find_element(*self.COMPANY_DROPDOWN).click()
        company_element = (By.CSS_SELECTOR, f"#company_id option[value='{company}']")
        self.wait.for_visible(company_element)
        self.find(company_element).click()
