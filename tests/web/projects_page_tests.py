from playwright.sync_api import expect


def test_valid_project_search(app: Application, login):
    valid_project_search = "Industrial"

    (app.projects_page.open()
     .is_loaded()
     .search_project(valid_project_search)
    )

    # Check that only projects which contain the search line are visible
    for project in app.projects_page.get_projects():
        if valid_project_search in project.title.text_content():
            expect(project.card).to_be_visible()
        else:
            expect(project.card).not_to_be_visible()


def test_invalid_project_search(app:Application, login):
    invalid_project_search = "lklfs;lfk"

    (app.projects_page.open()
     .is_loaded()
    .search_project(invalid_project_search)
    )

    expect(app.projects_page.project_cards.filter(visible=True)).to_have_count(0)
