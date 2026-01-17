from playwright.sync_api import Page, expect


class ProjectPage():
    def __init__(self, page: Page):
        self.page = page

        self.project_title = self.page.locator(".first h2")

        self.readme_block_resizer = self.page.locator(".resizer")
        self.readme_block_edit_btn = self.page.locator(".detail-view-actions [href*=readme]")
        self.readme_block_lets_start_btn = self.page.locator(".detail-view-content .primary-btn")
        self.readme_block_close_btn = self.page.locator(".back")

        self.input_new_suite_title = self.page.locator("[placeholder='First Suite']")
        self.add_suite_btn = self.page.get_by_role("button", name="Suite")

    def is_loaded(self):
        expect(self.project_title).to_be_visible(timeout=20_000)
        expect(self.page.locator(".mainnav-menu")).to_be_visible(timeout=10_000)
        expect(self.page.locator("#welcometotestomatio")).to_be_visible()
        expect(self.readme_block_resizer).to_be_visible()
        expect(self.readme_block_edit_btn).to_be_visible()
        expect(self.readme_block_close_btn).to_be_visible()
        expect(self.input_new_suite_title).to_be_visible()
        expect(self.add_suite_btn).to_be_visible()
