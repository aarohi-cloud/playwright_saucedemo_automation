import os
import pytest


@pytest.fixture(scope="session")
def base_url():
    """Provides the base URL — reads from env var so CI can override it."""
    return os.getenv("BASE_URL", "https://www.saucedemo.com")