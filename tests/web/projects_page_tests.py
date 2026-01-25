import pytest
from faker.proxy import Faker
from playwright.sync_api import expect


@pytest.mark.smoke
@pytest.mark.web
def test_valid_project_search(logged_app):
    valid_project_search = "Industrial"

    (logged_app.projects_page.open()
     .is_loaded()
     .search_project(valid_project_search)
    )

    # Check that only projects which contain the search line are visible
    for project in logged_app.projects_page.get_projects():
        if valid_project_search in project.title.text_content():
            expect(project.card).to_be_visible()
        else:
            expect(project.card).not_to_be_visible()


@pytest.mark.regression
@pytest.mark.web
def test_invalid_project_search(logged_app):
    invalid_project_search = Faker().password(length=6)  # "lklfs;lfk"

    (logged_app.projects_page.open()
     .is_loaded()
     .search_project(invalid_project_search)
    )

    expect(logged_app.projects_page.project_cards.filter(visible=True)).to_have_count(0)


@pytest.mark.regression
@pytest.mark.web
def test_projects_company_switch(logged_app):
    default_company = "QA Club Lviv"
    default_subscription = "Enterprise plan"
    free_projects_company = "Free Projects"
    free_subscription = "free plan"

    projects_page = logged_app.projects_page
    (projects_page.open()
     .is_loaded()
     )

    expect(projects_page.company_dropdown.locator("option:checked")).to_have_text(default_company)
    expect(projects_page.current_subscription).to_have_text(default_subscription)

    projects_page.select_company(projects_page.company_options.free_projects)

    expect(projects_page.company_dropdown.locator("option:checked")).to_have_text(free_projects_company)
    expect(projects_page.current_subscription).to_have_text(free_subscription)
    expect(projects_page.create_company_btn).to_be_visible()
