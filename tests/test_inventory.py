"""
Inventory page tests for Sauce Demo application.
Tests product display, sorting, and navigation to product details.
"""

import pytest
from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage
from pages.product_detail_page import ProductDetailPage
from tests.utils.test_data import VALID_USERS, PRODUCTS
from tests.utils.helpers import login_as


@pytest.mark.inventory
@pytest.mark.smoke
def test_inventory_page_loads(page):
    """
    Test that inventory page loads with all 6 products visible.
    Verifies that product list is displayed after login.
    """
    inventory_page = login_as(page, "standard")
    
    product_names = inventory_page.get_all_product_names()
    assert len(product_names) == 6, "Should display exactly 6 products"
    
    for expected_product in PRODUCTS:
        assert expected_product in product_names, f"Product '{expected_product}' should be visible"


@pytest.mark.inventory
@pytest.mark.regression
def test_sort_products_az(page):
    """
    Test that products can be sorted A-Z by name.
    Verifies that products are in alphabetical order.
    """
    inventory_page = login_as(page, "standard")
    
    inventory_page.sort_products('az')
    product_names = inventory_page.get_all_product_names()
    
    sorted_names = sorted(product_names)
    assert product_names == sorted_names, f"Products should be sorted A-Z. Got: {product_names}"


@pytest.mark.inventory
@pytest.mark.regression
def test_sort_products_za(page):
    """
    Test that products can be sorted Z-A by name.
    Verifies that products are in reverse alphabetical order.
    """
    inventory_page = login_as(page, "standard")
    
    inventory_page.sort_products('za')
    product_names = inventory_page.get_all_product_names()
    
    sorted_names = sorted(product_names, reverse=True)
    assert product_names == sorted_names, f"Products should be sorted Z-A. Got: {product_names}"


@pytest.mark.inventory
@pytest.mark.regression
def test_sort_by_price_low_high(page):
    """
    Test that products can be sorted by price low to high.
    Verifies that prices are in ascending order.
    """
    inventory_page = login_as(page, "standard")
    
    inventory_page.sort_products('lohi')
    prices = inventory_page.get_product_prices()
    
    sorted_prices = sorted(prices)
    assert prices == sorted_prices, f"Prices should be sorted low to high. Got: {prices}"


@pytest.mark.inventory
@pytest.mark.regression
def test_sort_by_price_high_low(page):
    """
    Test that products can be sorted by price high to low.
    Verifies that prices are in descending order.
    """
    inventory_page = login_as(page, "standard")
    
    inventory_page.sort_products('hilo')
    prices = inventory_page.get_product_prices()
    
    sorted_prices = sorted(prices, reverse=True)
    assert prices == sorted_prices, f"Prices should be sorted high to low. Got: {prices}"


@pytest.mark.inventory
@pytest.mark.regression
def test_product_detail_page(page):
    """
    Test that clicking on a product navigates to product detail page.
    Verifies that product detail page loads with correct product information.
    """
    inventory_page = login_as(page, "standard")
    
    # Click on first product
    all_products = page.query_selector_all('[data-test="inventory-item-name"]')
    assert len(all_products) > 0, "Should have at least one product"
    
    first_product_name = all_products[0].inner_text()
    all_products[0].click()
    page.wait_for_load_state("networkidle")
    
    # Verify on detail page
    product_detail_page = ProductDetailPage(page)
    detail_name = product_detail_page.get_product_name()
    assert detail_name == first_product_name, f"Should display correct product on detail page"


@pytest.mark.inventory
@pytest.mark.regression
def test_add_product_from_detail_page(page):
    """
    Test that user can add product to cart from product detail page.
    Verifies that add to cart button works on detail page.
    """
    inventory_page = login_as(page, "standard")
    
    # Navigate to product detail
    all_products = page.query_selector_all('[data-test="inventory-item-name"]')
    all_products[0].click()
    page.wait_for_load_state("networkidle")
    
    product_detail_page = ProductDetailPage(page)
    initial_cart_count = inventory_page.get_cart_count()
    
    # Add to cart from detail page
    product_detail_page.add_to_cart()
    page.wait_for_timeout(500)
    
    # Go back to inventory and verify cart updated
    product_detail_page.go_back()
    page.wait_for_load_state("networkidle")
    
    inventory_page = InventoryPage(page)
    updated_cart_count = inventory_page.get_cart_count()
    assert updated_cart_count == initial_cart_count + 1, "Cart count should increment by 1"
