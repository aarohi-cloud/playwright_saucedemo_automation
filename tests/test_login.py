"""
Login page tests for Sauce Demo application.
Tests user authentication, error handling, and logout functionality.
"""

import pytest
from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage
from tests.utils.test_data import VALID_USERS, INVALID_CREDENTIALS


@pytest.mark.login
@pytest.mark.smoke
def test_valid_login_standard_user(page, base_url):
    """
    Test that a standard user can successfully login.
    Verifies that the inventory page loads after login.
    """
    login_page = LoginPage(page)
    login_page.navigate()
    
    credentials = VALID_USERS["standard"]
    login_page.login(credentials["username"], credentials["password"])
    
    assert login_page.is_login_successful(), "Inventory page should load after successful login"


@pytest.mark.login
@pytest.mark.regression
def test_locked_out_user(page):
    """
    Test that a locked out user cannot login and sees appropriate error message.
    Verifies error handling for locked user accounts.
    """
    login_page = LoginPage(page)
    login_page.navigate()
    
    credentials = VALID_USERS["locked"]
    login_page.login(credentials["username"], credentials["password"])
    
    error_msg = login_page.get_error_message()
    assert "locked out" in error_msg.lower(), "Should display locked out user error message"
    assert not login_page.is_login_successful(), "Should not navigate to inventory page"


@pytest.mark.login
@pytest.mark.regression
def test_invalid_username(page):
    """
    Test that invalid username shows error message.
    Verifies that login fails with non-existent username.
    """
    login_page = LoginPage(page)
    login_page.navigate()
    
    invalid_cred = {"username": "nonexistent_user", "password": "secret_sauce"}
    login_page.login(invalid_cred["username"], invalid_cred["password"])
    
    error_msg = login_page.get_error_message()
    assert error_msg, "Error message should be displayed"
    assert not login_page.is_login_successful(), "Should not navigate to inventory page"


@pytest.mark.login
@pytest.mark.regression
def test_invalid_password(page):
    """
    Test that invalid password shows error message.
    Verifies that login fails with incorrect password.
    """
    login_page = LoginPage(page)
    login_page.navigate()
    
    invalid_cred = {"username": "standard_user", "password": "wrong_password"}
    login_page.login(invalid_cred["username"], invalid_cred["password"])
    
    error_msg = login_page.get_error_message()
    assert error_msg, "Error message should be displayed"
    assert not login_page.is_login_successful(), "Should not navigate to inventory page"


@pytest.mark.login
@pytest.mark.regression
def test_empty_username(page):
    """
    Test that empty username field shows error message.
    Verifies validation for empty username input.
    """
    login_page = LoginPage(page)
    login_page.navigate()
    
    login_page.login("", "secret_sauce")
    
    error_msg = login_page.get_error_message()
    assert error_msg, "Error message should be displayed for empty username"


@pytest.mark.login
@pytest.mark.regression
def test_empty_password(page):
    """
    Test that empty password field shows error message.
    Verifies validation for empty password input.
    """
    login_page = LoginPage(page)
    login_page.navigate()
    
    login_page.login("standard_user", "")
    
    error_msg = login_page.get_error_message()
    assert error_msg, "Error message should be displayed for empty password"


@pytest.mark.login
@pytest.mark.regression
def test_both_fields_empty(page):
    """
    Test that both empty fields show error message.
    Verifies validation when username and password are both empty.
    """
    login_page = LoginPage(page)
    login_page.navigate()
    
    login_page.login("", "")
    
    error_msg = login_page.get_error_message()
    assert error_msg, "Error message should be displayed when both fields are empty"


@pytest.mark.login
@pytest.mark.smoke
def test_logout(page):
    """
    Test that user can logout and return to login page.
    Verifies that logout functionality works correctly.
    """
    # Login first
    login_page = LoginPage(page)
    login_page.navigate()
    
    credentials = VALID_USERS["standard"]
    login_page.login(credentials["username"], credentials["password"])
    
    assert login_page.is_login_successful(), "Should successfully login"
    
    # Click menu and logout
    page.click('.bm-burger-button')
    page.wait_for_selector('[data-test="logout-sidebar-link"]', timeout=5000)
    page.click('[data-test="logout-sidebar-link"]')
    page.wait_for_load_state("networkidle")
    
    # Verify back on login page
    assert page.query_selector('input[data-test="username"]'), "Should be back on login page"
