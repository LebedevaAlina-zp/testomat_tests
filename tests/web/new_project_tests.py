from faker import Faker
from playwright.sync_api import Page

from src.web.pages.new_project_page import NewProjectPage, ProjectType
from src.web.pages.project_page import ProjectPage


def test_create_new_project_positive(page: Page, login):
    valid_project_title = Faker().company()

    (NewProjectPage(page)
     .open()
     .is_loaded()
     .create_new_project(valid_project_title, ProjectType.CLASSICAL)
     )

    (ProjectPage(page)
     .is_loaded()
     .verify_project_title_is(valid_project_title)
     .readme_block_close_btn.click()
     )
