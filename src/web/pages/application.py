from playwright.sync_api import Page

from src.web.pages.home_page import HomePage
from src.web.pages.project_page import ProjectPage
from src.web.pages.login_page import LoginPage
from src.web.pages.new_project_page import NewProjectPage
from src.web.pages.projects_page import ProjectsPage


class Application:
    def __init__(self, page: Page):
        self.home_page = HomePage(page)
        self.project_page = ProjectPage(page)
        self.login_page = LoginPage(page)
        self.new_project_page = NewProjectPage(page)
        self.projects_page = ProjectsPage(page)
