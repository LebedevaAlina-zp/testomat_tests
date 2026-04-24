import pytest
from selenium.common import NoSuchElementException, StaleElementReferenceException
from selenium.webdriver.common.by import By
from selenium.webdriver.ie.webdriver import WebDriver
from selenium.webdriver.support import expected_conditions as expected_conditions
from selenium.webdriver.support.wait import WebDriverWait

from tests.fixtures import Config


@pytest.mark.regression
@pytest.mark.selenium
def test_selenium_login_and_search(driver: WebDriver, configs: Config):
    wait = WebDriverWait(
        driver,
        15,
        poll_frequency=0.5,
        ignored_exceptions=[NoSuchElementException, StaleElementReferenceException],
    )

    driver.get(configs.login_url)
    driver.find_element(By.CSS_SELECTOR, "#content-desktop #user_email").send_keys(configs.email)
    driver.find_element(By.CSS_SELECTOR, "#content-desktop #user_password").send_keys(
        configs.password
    )
    driver.find_element(By.CSS_SELECTOR, "#content-desktop [value='Sign In']").click()
    wait.until(
        expected_conditions.visibility_of_element_located(
            (By.CSS_SELECTOR, "#content-desktop .common-flash-success")
        )
    )

    target_project = "Manufacture light"
    driver.find_element(By.CSS_SELECTOR, "#content-desktop #search").send_keys(target_project)

    driver.find_element(By.CSS_SELECTOR, f"[title='{target_project}']").click()

    wait.until(
        expected_conditions.visibility_of_element_located(
            (By.CSS_SELECTOR, f"[title='{target_project}']")
        )
    )

    driver.quit()
