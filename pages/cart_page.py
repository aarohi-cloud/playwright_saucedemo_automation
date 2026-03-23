from playwright.sync_api import Page
from typing import List, Dict


class CartPage:
    """Page object for Sauce Demo cart page."""

    def __init__(self, page: Page):
        self.page = page

    # Locators
    CART_ITEMS_CONTAINER = '[data-test="cart-list"]'
    CART_ITEM_ROW = '.cart_item'
    ITEM_NAME = '[data-test="inventory-item-name"]'
    ITEM_PRICE = '[data-test="inventory-item-price"]'
    ITEM_QUANTITY = '.cart_quantity'
    REMOVE_BUTTON = '[data-test^="remove"]'
    CHECKOUT_BUTTON = '[data-test="checkout"]'
    CONTINUE_SHOPPING_BUTTON = '[data-test="continue-shopping"]'

    def get_cart_items(self) -> List[Dict[str, str]]:
        """Get all items currently in the cart.
        
        Returns:
            List of dictionaries containing item details (name, price, quantity)
        """
        items = []
        cart_rows = self.page.query_selector_all(self.CART_ITEM_ROW)
        
        for row in cart_rows:
            name_elem = row.query_selector(self.ITEM_NAME)
            price_elem = row.query_selector(self.ITEM_PRICE)
            qty_elem = row.query_selector(self.ITEM_QUANTITY)
            
            item_dict = {
                'name': name_elem.inner_text() if name_elem else '',
                'price': price_elem.inner_text() if price_elem else '',
                'quantity': qty_elem.inner_text() if qty_elem else '1'
            }
            items.append(item_dict)
        
        return items

    def remove_item(self, item_name: str) -> None:
        """Remove a specific item from cart by name.
        
        Args:
            item_name: Name of the item to remove
        """
        cart_rows = self.page.query_selector_all(self.CART_ITEM_ROW)
        
        for row in cart_rows:
            name_elem = row.query_selector(self.ITEM_NAME)
            if name_elem and item_name in name_elem.inner_text():
                remove_btn = row.query_selector(self.REMOVE_BUTTON)
                if remove_btn:
                    remove_btn.click()
                    return

    def proceed_to_checkout(self) -> None:
        """Click on checkout button to proceed to checkout page."""
        self.page.click(self.CHECKOUT_BUTTON)
        self.page.wait_for_load_state("networkidle")

    def continue_shopping(self) -> None:
        """Click on continue shopping button to go back to inventory."""
        self.page.click(self.CONTINUE_SHOPPING_BUTTON)
        self.page.wait_for_load_state("networkidle")

    def get_item_count(self) -> int:
        """Get the number of items in the cart.
        
        Returns:
            Number of items in cart
        """
        cart_rows = self.page.query_selector_all(self.CART_ITEM_ROW)
        return len(cart_rows)
