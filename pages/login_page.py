from playwright.sync_api import Page, expect
from pages.base_page import BasePage, BASE_URL


class LoginPage(BasePage):
    """Page object for Sauce Demo login page."""

    def __init__(self, page: Page):
        super().__init__(page)

    # Locators
    USERNAME_INPUT = 'input[data-test="username"]'
    PASSWORD_INPUT = 'input[data-test="password"]'
    LOGIN_BUTTON = 'input[data-test="login-button"]'
    ERROR_MESSAGE = '.error-message-container'

    def navigate(self) -> None:
        """Navigate to the login page."""
        self.navigate_to(BASE_URL)

    def login(self, username: str, password: str) -> None:
        """Login with provided credentials.

        Args:
            username: Username to login with
            password: Password to login with
        """
        self.safe_fill(self.page.locator(self.USERNAME_INPUT), username)
        self.safe_fill(self.page.locator(self.PASSWORD_INPUT), password)
        self.safe_click(self.page.locator(self.LOGIN_BUTTON))
        self.page.wait_for_load_state("networkidle")

    def get_error_message(self) -> str:
        """Get error message text from login page.

        Returns:
            Error message text or empty string if not found
        """
        error_element = self.page.query_selector(self.ERROR_MESSAGE)
        if error_element:
            return error_element.inner_text()
        return ""

    def is_login_successful(self) -> bool:
        """Check if login was successful by verifying inventory page load.

        Returns:
            True if on inventory page, False otherwise
        """
        try:
            self.page.wait_for_selector('[data-test="inventory-list"]', timeout=5000)
            return True
        except Exception:
            return False
