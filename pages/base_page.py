"""
Base page class — all page objects inherit from this.
"""
import time
from typing import Any, Optional
from playwright.sync_api import Page, Locator, expect

BASE_URL = "https://www.saucedemo.com"
DEFAULT_TIMEOUT = 10_000


class BasePage:
    def __init__(self, page: Page) -> None:
        self.page = page

    def navigate_to(self, url: str, timeout: int = DEFAULT_TIMEOUT) -> None:
        self.page.goto(url, timeout=timeout)
        self.page.wait_for_load_state("networkidle", timeout=timeout)

    def safe_fill(self, locator: Locator, value: str, timeout: int = DEFAULT_TIMEOUT) -> None:
        expect(locator).to_be_visible(timeout=timeout)
        locator.fill(value)

    def safe_click(self, locator: Locator, timeout: int = DEFAULT_TIMEOUT) -> None:
        expect(locator).to_be_visible(timeout=timeout)
        locator.click()

    def safe_select(self, locator: Locator, value: str, timeout: int = DEFAULT_TIMEOUT) -> None:
        expect(locator).to_be_visible(timeout=timeout)
        locator.select_option(value)

    def get_text(self, locator: Locator, timeout: int = DEFAULT_TIMEOUT) -> str:
        expect(locator).to_be_visible(timeout=timeout)
        return locator.text_content() or ""

    def is_visible(self, locator: Locator, timeout: int = DEFAULT_TIMEOUT) -> bool:
        try:
            expect(locator).to_be_visible(timeout=timeout)
            return True
        except Exception:
            return False

    def retry_action(self, action: callable, max_retries: int = 3, delay: float = 1.0) -> Any:
        last_exc: Optional[Exception] = None
        for attempt in range(max_retries + 1):
            try:
                return action()
            except Exception as exc:
                last_exc = exc
                if attempt < max_retries:
                    time.sleep(delay)
                    delay *= 2
        raise last_exc
