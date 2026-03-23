from playwright.sync_api import Page


class CheckoutPage:
    """Page object for Sauce Demo checkout pages (step one and step two)."""

    def __init__(self, page: Page):
        self.page = page

    # Locators - Checkout Step One
    FIRST_NAME_INPUT = '[data-test="firstName"]'
    LAST_NAME_INPUT = '[data-test="lastName"]'
    POSTAL_CODE_INPUT = '[data-test="postalCode"]'
    CONTINUE_BUTTON = '[data-test="continue"]'
    
    # Locators - Checkout Step Two
    FINISH_BUTTON = '[data-test="finish"]'
    CART_LIST = '[data-test="cart-list"]'
    ITEM_TOTAL = '.summary_subtotal_label'
    TAX_TOTAL = '.summary_tax_label'
    TOTAL_PRICE = '.summary_total_label'
    
    # Locators - Order Confirmation
    CONFIRMATION_MESSAGE = '[data-test="complete-header"]'
    BACK_HOME_BUTTON = '[data-test="back-to-products"]'

    def fill_information(self, first_name: str, last_name: str, zip_code: str) -> None:
        """Fill in checkout information on step one.
        
        Args:
            first_name: First name
            last_name: Last name
            zip_code: Zip or postal code
        """
        self.page.fill(self.FIRST_NAME_INPUT, first_name)
        self.page.fill(self.LAST_NAME_INPUT, last_name)
        self.page.fill(self.POSTAL_CODE_INPUT, zip_code)

    def continue_checkout(self) -> None:
        """Click continue button to proceed to checkout step two."""
        self.page.click(self.CONTINUE_BUTTON)
        self.page.wait_for_load_state("networkidle")

    def finish_order(self) -> None:
        """Click finish button to complete the order."""
        self.page.click(self.FINISH_BUTTON)
        self.page.wait_for_load_state("networkidle")

    def get_confirmation_message(self) -> str:
        """Get the order confirmation message.
        
        Returns:
            Confirmation message text
        """
        confirmation = self.page.query_selector(self.CONFIRMATION_MESSAGE)
        if confirmation:
            return confirmation.inner_text()
        return ""

    def get_total_price(self) -> str:
        """Get the total order price.
        
        Returns:
            Total price text including currency
        """
        total_elem = self.page.query_selector(self.TOTAL_PRICE)
        if total_elem:
            return total_elem.inner_text()
        return ""

    def get_subtotal_price(self) -> str:
        """Get the subtotal (items only) price.
        
        Returns:
            Subtotal price text including currency
        """
        subtotal_elem = self.page.query_selector(self.ITEM_TOTAL)
        if subtotal_elem:
            return subtotal_elem.inner_text()
        return ""

    def get_tax_amount(self) -> str:
        """Get the tax amount.
        
        Returns:
            Tax amount text including currency
        """
        tax_elem = self.page.query_selector(self.TAX_TOTAL)
        if tax_elem:
            return tax_elem.inner_text()
        return ""

    def back_to_products(self) -> None:
        """Click back to products button after order completion."""
        self.page.click(self.BACK_HOME_BUTTON)
        self.page.wait_for_load_state("networkidle")
