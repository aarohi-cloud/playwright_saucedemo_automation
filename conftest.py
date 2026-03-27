"""
conftest.py — session configuration for pytest-playwright.
pytest-playwright automatically provides page, browser, context fixtures.
"""
from pathlib import Path
import pytest

# Load .env for local dev — CI uses real env vars directly
try:
    from dotenv import load_dotenv
    load_dotenv(Path(__file__).parent / ".env")
except ImportError:
    pass


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """On test failure, attach a full-page screenshot to Allure."""
    outcome = yield
    report = outcome.get_result()
    if report.when == "call" and report.failed:
        try:
            page = item.funcargs.get("page")
            if page:
                screenshot = page.screenshot(full_page=True)
                try:
                    import allure
                    allure.attach(
                        screenshot,
                        name="failure_screenshot",
                        attachment_type=allure.attachment_type.PNG,
                    )
                except ImportError:
                    pass
        except Exception:
            pass


def pytest_sessionfinish(session, exitstatus):
    """Send email report after run if EMAIL_ENABLED=true in .env"""
    try:
        from utils.email_reporter import send_email_report
        send_email_report(exitstatus=int(exitstatus))
    except Exception:
        pass
