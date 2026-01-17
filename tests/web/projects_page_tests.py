from playwright.sync_api import Page, expect

from src.web.pages.projects_page import ProjectsPage


def test_valid_project_search(page: Page, login):
    valid_project_search = "Industrial"

    projects_page = ProjectsPage(page)
    projects_page.open()
    projects_page.is_loaded()

    projects_page.search_project(valid_project_search)

    # Check that only projects which contain the search line are visible
    for project in projects_page.get_projects():
        if valid_project_search in project.title.text_content():
            expect(project.card).to_be_visible()
        else:
            expect(project.card).not_to_be_visible()


def test_invalid_project_search(page: Page, login):
    invalid_project_search = "lklfs;lfk"

    projects_page = ProjectsPage(page)
    projects_page.open()
    projects_page.is_loaded()

    projects_page.search_project(invalid_project_search)

    expect(projects_page.project_cards.filter(visible=True)).to_have_count(0)
