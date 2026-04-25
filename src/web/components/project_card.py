import allure
from playwright.sync_api import Locator


class ProjectCard:
    def __init__(self, card: Locator):
        self.card = card

    @property
    def title(self) -> Locator:
        return self.card.locator("h3")

    @property
    def tests_count(self) -> Locator:
        return self.card.locator("p")

    @property
    def link(self) -> Locator:
        return self.card.locator("a")

    @allure.step
    def open(self):
        self.link.click()
