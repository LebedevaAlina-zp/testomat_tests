from faker import Faker
from playwright.sync_api import Page, expect

from src.web.pages.new_project_page import NewProjectPage, ProjectType
from src.web.pages.project_page import ProjectPage


def test_create_new_project_positive(page: Page, login):
    new_project_page = NewProjectPage(page)
    new_project_page.open()
    new_project_page.is_loaded()

    valid_project_title = Faker().company()
    print(valid_project_title)

    new_project_page.create_new_project(valid_project_title, ProjectType.CLASSICAL)

    project_page = ProjectPage(page)
    project_page.is_loaded()
    expect(project_page.project_title).to_have_text(valid_project_title)
