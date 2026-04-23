import pytest
from playwright.sync_api import expect

from src.web import Application


@pytest.mark.smoke
@pytest.mark.web
def test_free_plan_is_available(free_plan_app: Application):
    free_projects_company = "Free Projects"
    free_subscription = "free plan"
    free_plan_hint_message = "You have a free subscription"

    projects_page = free_plan_app.projects_page
    projects_page.open()

    projects_page.expect_selected_company(free_projects_company)
    projects_page.expect_current_subscription(free_subscription)

    expect(projects_page.create_company_btn).to_be_visible()

    projects_page.current_subscription.hover(timeout=2000)
    expect(projects_page.page.get_by_text(free_plan_hint_message)).to_be_visible()
