import pytest
from faker import Faker

from src.web.pages import ProjectType


@pytest.mark.smoke
@pytest.mark.web
def test_create_new_project_positive(logged_app):
    valid_project_title = Faker().company()

    (logged_app.new_project_page.open()
     .is_loaded()
     .create_new_project(valid_project_title, ProjectType.CLASSICAL)
     )

    (logged_app.project_page.is_loaded()
     .verify_project_title_is(valid_project_title)
     .readme_block_close_btn.click()
     )


@pytest.mark.regression
@pytest.mark.web
def test_new_project_side_bar_navigation(logged_app):
    target_project_name = "Grocery, Outdoors & Shoes"
    logged_app.project_page.open(target_project_name)

    (logged_app.project_page.side_bar
     .is_loaded()
     .open_side_bar()
     .expect_tab_active("Tests")
     .click_requirements()
     .expect_tab_active("Requirements"))
