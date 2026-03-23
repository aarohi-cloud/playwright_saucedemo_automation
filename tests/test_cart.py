"""
Cart page tests for Sauce Demo application.
Tests adding/removing items, cart persistence, and cart interactions.
"""

import pytest
from pages.inventory_page import InventoryPage
from pages.cart_page import CartPage
from pages.product_detail_page import ProductDetailPage
from tests.utils.test_data import PRODUCTS
from tests.utils.helpers import login_as, add_products_to_cart


@pytest.mark.cart
@pytest.mark.smoke
def test_add_single_item_to_cart(page):
    """
    Test that user can add a single item to cart.
    Verifies that cart count increments to 1.
    """
    inventory_page = login_as(page, "standard")
    
    inventory_page.add_product_to_cart(PRODUCTS[0])
    cart_count = inventory_page.get_cart_count()
    
    assert cart_count == 1, "Cart should contain 1 item after adding one product"


@pytest.mark.cart
@pytest.mark.smoke
def test_add_multiple_items_to_cart(page):
    """
    Test that user can add multiple items to cart.
    Verifies that cart count increments correctly with each addition.
    """
    inventory_page = login_as(page, "standard")
    
    products_to_add = [PRODUCTS[0], PRODUCTS[1], PRODUCTS[2]]
    add_products_to_cart(inventory_page, products_to_add)
    
    cart_count = inventory_page.get_cart_count()
    assert cart_count == 3, "Cart should contain 3 items"


@pytest.mark.cart
@pytest.mark.regression
def test_remove_item_from_cart(page):
    """
    Test that user can remove items from cart.
    Verifies that cart is empty after removing all items.
    """
    inventory_page = login_as(page, "standard")
    
    # Add item
    inventory_page.add_product_to_cart(PRODUCTS[0])
    assert inventory_page.get_cart_count() == 1
    
    # Go to cart and remove
    inventory_page.go_to_cart()
    cart_page = CartPage(page)
    
    cart_items = cart_page.get_cart_items()
    assert len(cart_items) == 1
    
    cart_page.remove_item(cart_items[0]['name'])
    page.wait_for_timeout(500)
    
    remaining_items = cart_page.get_cart_items()
    assert len(remaining_items) == 0, "Cart should be empty after removing all items"


@pytest.mark.cart
@pytest.mark.regression
def test_cart_persists_after_navigation(page):
    """
    Test that cart items persist after navigating away and back.
    Verifies that cart data is maintained across page navigation.
    """
    inventory_page = login_as(page, "standard")
    
    # Add item to cart
    inventory_page.add_product_to_cart(PRODUCTS[0])
    initial_count = inventory_page.get_cart_count()
    
    # Navigate to product detail page
    all_products = page.query_selector_all('[data-test="inventory-item-name"]')
    all_products[1].click()
    page.wait_for_load_state("networkidle")
    
    product_detail_page = ProductDetailPage(page)
    product_detail_page.go_back()
    page.wait_for_load_state("networkidle")
    
    # Go to cart and verify item is still there
    inventory_page = InventoryPage(page)
    assert inventory_page.get_cart_count() == initial_count, "Cart should persist after navigation"


@pytest.mark.cart
@pytest.mark.regression
def test_cart_item_details(page):
    """
    Test that cart displays correct item details (name and price).
    Verifies that item information is accurate in the cart.
    """
    inventory_page = login_as(page, "standard")
    
    # Add item and go to cart
    inventory_page.add_product_to_cart(PRODUCTS[0])
    inventory_page.go_to_cart()
    
    cart_page = CartPage(page)
    cart_items = cart_page.get_cart_items()
    
    assert len(cart_items) == 1, "Should have 1 item in cart"
    assert cart_items[0]['name'] == PRODUCTS[0], f"Item name should be {PRODUCTS[0]}"
    assert '$' in cart_items[0]['price'], "Item should have price with currency symbol"


@pytest.mark.cart
@pytest.mark.regression
def test_continue_shopping(page):
    """
    Test that user can continue shopping from cart page.
    Verifies that continue shopping button returns to inventory.
    """
    inventory_page = login_as(page, "standard")
    
    # Add item and go to cart
    inventory_page.add_product_to_cart(PRODUCTS[0])
    inventory_page.go_to_cart()
    
    cart_page = CartPage(page)
    cart_page.continue_shopping()
    page.wait_for_load_state("networkidle")
    
    # Verify back on inventory page
    inventory_page = InventoryPage(page)
    products = inventory_page.get_all_product_names()
    assert len(products) == 6, "Should be back on inventory with all 6 products"


@pytest.mark.cart
@pytest.mark.regression
def test_cart_badge_updates(page):
    """
    Test that cart badge updates with each item addition.
    Verifies that badge count is accurate.
    """
    inventory_page = login_as(page, "standard")
    
    # Add items one by one and verify badge
    for i in range(1, 4):
        inventory_page.add_product_to_cart(PRODUCTS[i-1])
        cart_count = inventory_page.get_cart_count()
        assert cart_count == i, f"Cart badge should show {i} items"


@pytest.mark.cart
@pytest.mark.regression
def test_remove_all_items(page):
    """
    Test that user can remove all items from cart.
    Verifies that cart becomes empty after removing multiple items.
    """
    inventory_page = login_as(page, "standard")
    
    # Add multiple items
    add_products_to_cart(inventory_page, [PRODUCTS[0], PRODUCTS[1]])
    assert inventory_page.get_cart_count() == 2
    
    # Go to cart and remove all
    inventory_page.go_to_cart()
    cart_page = CartPage(page)
    
    cart_items = cart_page.get_cart_items()
    for item in cart_items:
        cart_page.remove_item(item['name'])
        page.wait_for_timeout(300)
    
    remaining_items = cart_page.get_cart_items()
    assert len(remaining_items) == 0, "Cart should be completely empty"
