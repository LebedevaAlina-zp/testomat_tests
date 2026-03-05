from typing import Self

from playwright.sync_api import Page, expect


class ReadmeBlock:
    def __init__(self, page: Page):
        self.page = page

        self.readme_block_resizer = self.page.locator(".resizer")
        self.readme_block_edit_btn = self.page.locator(
            ".detail-view-actions [href*=readme]"
        )
        self.readme_block_lets_start_btn = self.page.locator(
            ".detail-view-content .primary-btn"
        )
        self.readme_block_close_btn = self.page.locator(".back")

    def is_loaded(self) -> Self:
        expect(self.readme_block_resizer).to_be_visible()
        expect(self.readme_block_edit_btn).to_be_visible()
        expect(self.readme_block_lets_start_btn).to_be_visible()
        expect(self.readme_block_close_btn).to_be_visible()
        return self

    def click_lets_start(self):
        self.readme_block_lets_start_btn.click()
        return self

    def click_close(self):
        self.readme_block_close_btn.click()
