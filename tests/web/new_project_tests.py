import pytest
from faker import Faker
from playwright.sync_api import Page

from src.web.pages.new_project_page import NewProjectPage, ProjectType
from src.web.pages.project_page import ProjectPage


@pytest.mark.smoke
@pytest.mark.web
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


@pytest.mark.regression
@pytest.mark.web
def test_new_project_side_bar_navigation(page:Page, login, app: Application):
    target_project_name = "Grocery, Outdoors & Shoes"
    app.project_page.open(target_project_name)

    (app.project_page.side_bar
     .is_loaded()
     .open_side_bar()
     .expect_tab_active("Tests")
     .click_requirements()
     .expect_tab_active("Requirements"))
    