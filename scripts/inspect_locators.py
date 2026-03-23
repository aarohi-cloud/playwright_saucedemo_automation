"""
Script to inspect SauceDemo website and extract all locators.
Run this script to gather CSS selectors for all required elements.
"""

from playwright.sync_api import sync_playwright
import json

def extract_locators():
    """Extract all locators from SauceDemo website."""
    
    locators = {
        "login_page": {},
        "inventory_page": {},
        "cart_page": {},
        "checkout_page": {}
    }
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context(viewport={"width": 1280, "height": 720})
        page = context.new_page()
        
        # ===== LOGIN PAGE =====
        print("\n=== Inspecting LOGIN PAGE ===")
        page.goto("https://www.saucedemo.com/")
        page.wait_for_load_state("networkidle")
        
        # Username field
        username_locator = page.query_selector('input[data-test="username"]')
        if username_locator:
            locators["login_page"]["username_input"] = 'input[data-test="username"]'
        else:
            username_locator = page.query_selector('input[id="user-name"]')
            if username_locator:
                locators["login_page"]["username_input"] = 'input[id="user-name"]'
        
        # Password field
        password_locator = page.query_selector('input[data-test="password"]')
        if password_locator:
            locators["login_page"]["password_input"] = 'input[data-test="password"]'
        else:
            password_locator = page.query_selector('input[id="password"]')
            if password_locator:
                locators["login_page"]["password_input"] = 'input[id="password"]'
        
        # Login button
        login_btn = page.query_selector('input[data-test="login-button"]')
        if login_btn:
            locators["login_page"]["login_button"] = 'input[data-test="login-button"]'
        else:
            login_btn = page.query_selector('input[type="submit"]')
            if login_btn:
                locators["login_page"]["login_button"] = 'input[type="submit"]'
        
        # Error message container
        error_msg = page.query_selector('[data-test="error"]')
        if error_msg:
            locators["login_page"]["error_message"] = '[data-test="error"]'
        else:
            error_msg = page.query_selector(".error-message-container")
            if error_msg:
                locators["login_page"]["error_message"] = ".error-message-container"
        
        print("Login Page Locators Found:")
        for key, value in locators["login_page"].items():
            print(f"  {key}: {value}")
        
        # ===== LOGIN & NAVIGATE TO INVENTORY =====
        print("\n=== Logging in and inspecting INVENTORY PAGE ===")
        page.fill('input[data-test="username"]', "standard_user")
        page.fill('input[data-test="password"]', "secret_sauce")
        page.click('input[data-test="login-button"]')
        page.wait_for_load_state("networkidle")
        
        # Product container/items
        products_container = page.query_selector('[data-test="inventory-list"]')
        if products_container:
            locators["inventory_page"]["products_container"] = '[data-test="inventory-list"]'
        else:
            products_container = page.query_selector('.inventory_list')
            if products_container:
                locators["inventory_page"]["products_container"] = '.inventory_list'
        
        # Individual product item
        product_item = page.query_selector('[data-test="inventory-item"]')
        if product_item:
            locators["inventory_page"]["product_item"] = '[data-test="inventory-item"]'
        else:
            product_item = page.query_selector('.inventory_item')
            if product_item:
                locators["inventory_page"]["product_item"] = '.inventory_item'
        
        # Product title
        product_title = page.query_selector('[data-test="inventory-item-name"]')
        if product_title:
            locators["inventory_page"]["product_title"] = '[data-test="inventory-item-name"]'
        else:
            product_title = page.query_selector('.inventory_item_name')
            if product_title:
                locators["inventory_page"]["product_title"] = '.inventory_item_name'
        
        # Add to cart button
        add_to_cart_btn = page.query_selector('[data-test="add-to-cart-sauce-labs-backpack"]')
        if add_to_cart_btn:
            locators["inventory_page"]["add_to_cart_button"] = '[data-test="add-to-cart-sauce-labs-backpack"]'
        else:
            add_to_cart_btn = page.query_selector('button:has-text("Add to cart")')
            if add_to_cart_btn:
                locators["inventory_page"]["add_to_cart_button"] = 'button:has-text("Add to cart")'
        
        # Cart icon/link
        cart_icon = page.query_selector('[data-test="shopping-cart-link"]')
        if cart_icon:
            locators["inventory_page"]["shopping_cart_icon"] = '[data-test="shopping-cart-link"]'
        else:
            cart_icon = page.query_selector('.shopping_cart_link')
            if cart_icon:
                locators["inventory_page"]["shopping_cart_icon"] = '.shopping_cart_link'
        
        # Cart item count badge
        cart_badge = page.query_selector('[data-test="shopping-cart-badge"]')
        if cart_badge:
            locators["inventory_page"]["cart_item_count_badge"] = '[data-test="shopping-cart-badge"]'
        else:
            cart_badge = page.query_selector('.shopping_cart_badge')
            if cart_badge:
                locators["inventory_page"]["cart_item_count_badge"] = '.shopping_cart_badge'
        
        print("Inventory Page Locators Found:")
        for key, value in locators["inventory_page"].items():
            print(f"  {key}: {value}")
        
        # ===== ADD ITEM TO CART & GO TO CART PAGE =====
        print("\n=== Adding item to cart and inspecting CART PAGE ===")
        page.click('[data-test="add-to-cart-sauce-labs-backpack"]')
        page.click('[data-test="shopping-cart-link"]')
        page.wait_for_load_state("networkidle")
        
        # Cart item rows
        cart_item = page.query_selector('[data-test="cart-list"]')
        if cart_item:
            locators["cart_page"]["cart_items_container"] = '[data-test="cart-list"]'
        else:
            cart_item = page.query_selector('.cart_list')
            if cart_item:
                locators["cart_page"]["cart_items_container"] = '.cart_list'
        
        # Individual cart item row
        cart_row = page.query_selector('[data-test="cart-item"]')
        if cart_row:
            locators["cart_page"]["cart_item_row"] = '[data-test="cart-item"]'
        else:
            cart_row = page.query_selector('.cart_item')
            if cart_row:
                locators["cart_page"]["cart_item_row"] = '.cart_item'
        
        # Item name in cart
        item_name = page.query_selector('[data-test="inventory-item-name"]')
        if item_name:
            locators["cart_page"]["item_name"] = '[data-test="inventory-item-name"]'
        else:
            item_name = page.query_selector('.inventory_item_name')
            if item_name:
                locators["cart_page"]["item_name"] = '.inventory_item_name'
        
        # Item price in cart
        item_price = page.query_selector('[data-test="inventory-item-price"]')
        if item_price:
            locators["cart_page"]["item_price"] = '[data-test="inventory-item-price"]'
        else:
            item_price = page.query_selector('.inventory_item_price')
            if item_price:
                locators["cart_page"]["item_price"] = '.inventory_item_price'
        
        # Remove button
        remove_btn = page.query_selector('[data-test="remove-sauce-labs-backpack"]')
        if remove_btn:
            locators["cart_page"]["remove_button"] = '[data-test="remove-sauce-labs-backpack"]'
        else:
            remove_btn = page.query_selector('button:has-text("Remove")')
            if remove_btn:
                locators["cart_page"]["remove_button"] = 'button:has-text("Remove")'
        
        # Checkout button
        checkout_btn = page.query_selector('[data-test="checkout"]')
        if checkout_btn:
            locators["cart_page"]["checkout_button"] = '[data-test="checkout"]'
        
        # Continue shopping button
        continue_shopping = page.query_selector('[data-test="continue-shopping"]')
        if continue_shopping:
            locators["cart_page"]["continue_shopping_button"] = '[data-test="continue-shopping"]'
        
        print("Cart Page Locators Found:")
        for key, value in locators["cart_page"].items():
            print(f"  {key}: {value}")
        
        # ===== CHECKOUT PAGE =====
        print("\n=== Inspecting CHECKOUT PAGE ===")
        page.click('[data-test="checkout"]')
        page.wait_for_load_state("networkidle")
        
        # First name input
        first_name = page.query_selector('[data-test="firstName"]')
        if first_name:
            locators["checkout_page"]["first_name_input"] = '[data-test="firstName"]'
        else:
            first_name = page.query_selector('input[placeholder="First Name"]')
            if first_name:
                locators["checkout_page"]["first_name_input"] = 'input[placeholder="First Name"]'
        
        # Last name input
        last_name = page.query_selector('[data-test="lastName"]')
        if last_name:
            locators["checkout_page"]["last_name_input"] = '[data-test="lastName"]'
        else:
            last_name = page.query_selector('input[placeholder="Last Name"]')
            if last_name:
                locators["checkout_page"]["last_name_input"] = 'input[placeholder="Last Name"]'
        
        # Postal code input
        postal_code = page.query_selector('[data-test="postalCode"]')
        if postal_code:
            locators["checkout_page"]["postal_code_input"] = '[data-test="postalCode"]'
        else:
            postal_code = page.query_selector('input[placeholder="Zip/Postal Code"]')
            if postal_code:
                locators["checkout_page"]["postal_code_input"] = 'input[placeholder="Zip/Postal Code"]'
        
        # Continue button (checkout info page)
        continue_btn = page.query_selector('[data-test="continue"]')
        if continue_btn:
            locators["checkout_page"]["continue_button"] = '[data-test="continue"]'
        
        # Finish button
        finish_btn = page.query_selector('[data-test="finish"]')
        if finish_btn:
            locators["checkout_page"]["finish_button"] = '[data-test="finish"]'
        
        # Order confirmation message
        confirmation = page.query_selector('[data-test="complete-header"]')
        if confirmation:
            locators["checkout_page"]["order_confirmation_message"] = '[data-test="complete-header"]'
        
        print("Checkout Page Locators Found:")
        for key, value in locators["checkout_page"].items():
            print(f"  {key}: {value}")
        
        browser.close()
    
    return locators

if __name__ == "__main__":
    locators = extract_locators()
    
    print("\n" + "="*60)
    print("COMPLETE LOCATORS JSON:")
    print("="*60)
    print(json.dumps(locators, indent=2))
    
    # Save to file
    with open("locators.json", "w") as f:
        json.dump(locators, f, indent=2)
    print("\nLocators saved to: locators.json")
