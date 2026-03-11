import pytest
from selenium import webdriver
from selenium.webdriver.ie.webdriver import WebDriver


@pytest.fixture(scope="function")
def driver() -> WebDriver:
    driver = webdriver.Chrome()
    driver.implicitly_wait(0)
    driver.set_window_size(1540, 820)
    yield driver
    driver.quit()
