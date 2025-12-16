from playwright.sync_api import Page, expect


def test_sign_in_with_invalid_creds(page: Page):
    page.goto('https://www.testomat.io')

    expect(page.get_by_text('Log in', exact=True)).to_be_visible()

    page.get_by_text('Log in', exact=True).click()

    page.locator("#content-desktop #user_email").fill("lebedeva.alina.zp@gmail.com")
    page.locator("#content-desktop #user_password").fill("kded;pdq")

    page.get_by_role("button", name="Sign In").click()

    expect(page.locator("#content-desktop .common-flash-info-right")).to_have_text("Invalid Email or password.")
