from playwright.sync_api import Page

from src.web.pages import HomePage, LoginPage, NewProjectPage, ProjectPage, ProjectsPage


class Application:
    def __init__(self, page: Page):
        self.home_page = HomePage(page)
        self.project_page = ProjectPage(page)
        self.login_page = LoginPage(page)
        self.new_project_page = NewProjectPage(page)
        self.projects_page = ProjectsPage(page)
