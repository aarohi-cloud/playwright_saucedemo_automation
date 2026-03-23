"""
Helper functions for Sauce Demo automation tests.
"""

from playwright.sync_api import Page
from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage
from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage
from tests.utils import test_data


def login_as(page: Page, user_type: str) -> InventoryPage:
    """
    Navigate to login page and login with specified user type.
    
    Args:
        page: Playwright page object
        user_type: Type of user - "standard", "locked", "problem", "performance"
    
    Returns:
        InventoryPage object after successful login
    
    Raises:
        ValueError: If invalid user_type is provided
    """
    if user_type not in test_data.VALID_USERS:
        raise ValueError(f"Invalid user_type: {user_type}. Must be one of {list(test_data.VALID_USERS.keys())}")
    
    login_page = LoginPage(page)
    login_page.navigate()
    
    credentials = test_data.VALID_USERS[user_type]
    login_page.login(credentials["username"], credentials["password"])
    
    return InventoryPage(page)


def add_products_to_cart(inventory_page: InventoryPage, product_names: list) -> None:
    """
    Add multiple products to cart by their names.
    
    Args:
        inventory_page: InventoryPage object
        product_names: List of product names to add to cart
    
    Example:
        add_products_to_cart(inventory_page, ["Sauce Labs Backpack", "Sauce Labs Bike Light"])
    """
    for product_name in product_names:
        inventory_page.add_product_to_cart(product_name)


def complete_checkout(checkout_page: CheckoutPage, info: dict = None) -> str:
    """
    Fill checkout information and complete the checkout process.
    
    Args:
        checkout_page: CheckoutPage object
        info: Dictionary with keys "first_name", "last_name", "zip"
              Defaults to test_data.CHECKOUT_INFO if not provided
    
    Returns:
        Confirmation message from the order completion page
    
    Example:
        confirmation = complete_checkout(checkout_page)
        confirmation = complete_checkout(checkout_page, 
                                        {"first_name": "Jane", "last_name": "Smith", "zip": "54321"})
    """
    if info is None:
        info = test_data.CHECKOUT_INFO
    
    checkout_page.fill_information(info["first_name"], info["last_name"], info["zip"])
    checkout_page.continue_checkout()
    checkout_page.finish_order()
    
    return checkout_page.get_confirmation_message()
