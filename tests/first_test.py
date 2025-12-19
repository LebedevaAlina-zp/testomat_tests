from playwright.sync_api import Page, expect


def test_sign_in_with_invalid_creds(page: Page):
    page.goto('https://www.testomat.io')

    expect(page.get_by_text('Log in', exact=True)).to_be_visible()

    page.get_by_text('Log in', exact=True).click()

    page.locator("#content-desktop #user_email").fill("lebedeva.alina.zp@gmail.com")
    page.locator("#content-desktop #user_password").fill("kded;pdq")
    page.get_by_role("button", name="Sign In").click()

    expect(page.locator("#content-desktop .common-flash-info-right")).to_have_text("Invalid Email or password.")


def test_search_project_in_company(page: Page):
    page.goto("https://app.testomat.io/users/sign_in")

    login_user(page, email="lebedeva.alina.zp@gmail.com", password="ololo")

    target_project = "Industrial & Jewelry"

    search_by_project(page, target_project)

    expect(page.get_by_role("heading", name=target_project)).to_be_visible()
    expect(page.locator("ul li h3").filter(visible=True)).to_have_text(target_project)


def test_should_be_possible_open_free_project(page: Page):
    page.goto("https://app.testomat.io/users/sign_in")
    login_user(page, email="lebedeva.alina.zp@gmail.com", password="ololo")
    page.locator("#company_id").click()
    page.locator("#company_id").select_option("Free Projects")

    expect(page.get_by_text("Create project")).to_be_visible()

    target_project = "Industrial & Jewelry"
    search_by_project(page, target_project)
    expect(page.get_by_role("heading", name=target_project)).to_be_hidden()


def search_by_project(page: Page, target_project: str):
    # expect(page.get_by_role("searchbox", name="Search")).to_be_visible()
    page.locator("#content-desktop #search").fill(target_project)


def open_homepage(page: Page):
    page.goto('https://www.testomat.io')


def login_user(page: Page, email: str, password: str):
    page.locator("#content-desktop #user_email").fill(email)
    page.locator("#content-desktop #user_password").fill(password)
    page.get_by_role("button", name="Sign In").click()
