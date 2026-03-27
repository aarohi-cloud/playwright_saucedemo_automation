from playwright.sync_api import Page
from pages.base_page import BasePage


class ProductDetailPage(BasePage):
    """Page object for Sauce Demo product detail page."""

    def __init__(self, page: Page):
        super().__init__(page)

    # Locators
    PRODUCT_NAME = '[data-test="inventory-item-name"]'
    PRODUCT_PRICE = '[data-test="inventory-item-price"]'
    PRODUCT_DESCRIPTION = '[data-test="inventory-item-desc"]'
    PRODUCT_IMAGE = '[data-test="inventory-item-img"]'
    ADD_TO_CART_BUTTON = '[data-test="add-to-cart"]'
    BACK_BUTTON = '[data-test="back-to-products"]'
    REMOVE_BUTTON = '[data-test="remove"]'

    def get_product_name(self) -> str:
        """Get the name of the product.

        Returns:
            Product name text
        """
        name_elem = self.page.query_selector(self.PRODUCT_NAME)
        if name_elem:
            return name_elem.inner_text()
        return ""

    def get_product_price(self) -> str:
        """Get the price of the product.

        Returns:
            Product price text including currency
        """
        price_elem = self.page.query_selector(self.PRODUCT_PRICE)
        if price_elem:
            return price_elem.inner_text()
        return ""

    def get_product_description(self) -> str:
        """Get the description of the product.

        Returns:
            Product description text
        """
        desc_elem = self.page.query_selector(self.PRODUCT_DESCRIPTION)
        if desc_elem:
            return desc_elem.inner_text()
        return ""

    def add_to_cart(self) -> None:
        """Click the add to cart button."""
        add_btn = self.page.query_selector(self.ADD_TO_CART_BUTTON)
        if add_btn:
            add_btn.click()
        else:
            # Try remove button if add button doesn't exist (item already in cart)
            remove_btn = self.page.query_selector(self.REMOVE_BUTTON)
            if remove_btn:
                remove_btn.click()

    def go_back(self) -> None:
        """Click the back button to return to inventory page."""
        self.safe_click(self.page.locator(self.BACK_BUTTON))
        self.page.wait_for_load_state("networkidle")
