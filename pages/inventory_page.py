from playwright.sync_api import Page
from typing import List
from pages.base_page import BasePage


class InventoryPage(BasePage):
    """Page object for Sauce Demo inventory page."""

    def __init__(self, page: Page):
        super().__init__(page)

    # Locators
    PRODUCTS_CONTAINER = '[data-test="inventory-list"]'
    PRODUCT_ITEM = '[data-test="inventory-item"]'
    PRODUCT_TITLE = '[data-test="inventory-item-name"]'
    PRODUCT_PRICE = '[data-test="inventory-item-price"]'
    ADD_TO_CART_BUTTON = '[data-test="add-to-cart"]'
    REMOVE_FROM_CART_BUTTON = '[data-test="remove"]'
    SHOPPING_CART_LINK = '[data-test="shopping-cart-link"]'
    CART_BADGE = '[data-test="shopping-cart-badge"]'
    SORT_SELECT = '[data-test="product-sort-container"]'

    def get_all_product_names(self) -> List[str]:
        """Get names of all products on the page.

        Returns:
            List of product names
        """
        product_name_elements = self.page.query_selector_all(self.PRODUCT_TITLE)
        product_names = [elem.inner_text() for elem in product_name_elements]
        return product_names

    def add_product_to_cart(self, product_name: str) -> None:
        """Add a specific product to cart by name.

        Args:
            product_name: Name of the product to add to cart
        """
        # Find the product item containing the product name
        product_items = self.page.query_selector_all(self.PRODUCT_ITEM)
        for item in product_items:
            title = item.query_selector(self.PRODUCT_TITLE)
            if title and product_name in title.inner_text():
                # Click the add to cart button within this item
                add_btn = item.query_selector('[data-test^="add-to-cart"]')
                if add_btn:
                    add_btn.click()
                    return

    def get_cart_count(self) -> int:
        """Get the current count of items in the cart.

        Returns:
            Number of items in cart, or 0 if badge not visible
        """
        badge = self.page.query_selector(self.CART_BADGE)
        if badge:
            try:
                return int(badge.inner_text())
            except Exception:
                return 0
        return 0

    def go_to_cart(self) -> None:
        """Click on shopping cart link to go to cart page."""
        self.safe_click(self.page.locator(self.SHOPPING_CART_LINK))
        self.page.wait_for_load_state("networkidle")

    def sort_products(self, option: str) -> None:
        """Sort products by the specified option.

        Args:
            option: Sort option - 'az', 'za', 'lohi' (low to high), 'hilo' (high to low)
        """
        sort_options = {
            'az': 'Name (A to Z)',
            'za': 'Name (Z to A)',
            'lohi': 'Price (low to high)',
            'hilo': 'Price (high to low)'
        }

        if option not in sort_options:
            raise ValueError(f"Invalid sort option: {option}")

        sort_value_map = {
            'az': 'az',
            'za': 'za',
            'lohi': 'lohi',
            'hilo': 'hilo'
        }

        self.safe_select(self.page.locator(self.SORT_SELECT), sort_value_map[option])
        self.page.wait_for_load_state("networkidle")

    def get_product_prices(self) -> List[float]:
        """Get prices of all products on the page.

        Returns:
            List of product prices as floats
        """
        price_elements = self.page.query_selector_all(self.PRODUCT_PRICE)
        prices = []
        for elem in price_elements:
            price_text = elem.inner_text().replace('$', '').strip()
            try:
                prices.append(float(price_text))
            except ValueError:
                pass
        return prices
