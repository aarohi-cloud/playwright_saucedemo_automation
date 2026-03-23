import pytest
from playwright.sync_api import sync_playwright, Browser, BrowserContext, Page


@pytest.fixture(scope="session")
def browser():
    """Fixture that provides a Playwright browser instance in headed mode."""
    playwright = sync_playwright().start()
    browser = playwright.chromium.launch(headless=False)
    yield browser
    browser.close()
    playwright.stop()


@pytest.fixture(scope="function")
def context(browser: Browser) -> BrowserContext:
    """Fixture that provides a new browser context with 1280x720 viewport."""
    ctx = browser.new_context(viewport={"width": 1280, "height": 720})
    yield ctx
    ctx.close()


@pytest.fixture(scope="function")
def page(context: BrowserContext) -> Page:
    """Fixture that provides a new page for each test."""
    return context.new_page()


@pytest.fixture
def base_url():
    """Fixture that provides the base URL for the SauceDemo application."""
    return "https://www.saucedemo.com"
