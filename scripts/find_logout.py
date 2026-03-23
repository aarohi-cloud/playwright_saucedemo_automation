"""
Script to find the correct logout locator on Sauce Demo.
"""

from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page = browser.new_page(viewport={"width": 1280, "height": 720})
    
    # Login
    page.goto("https://www.saucedemo.com/")
    page.fill('input[data-test="username"]', "standard_user")
    page.fill('input[data-test="password"]', "secret_sauce")
    page.click('input[data-test="login-button"]')
    page.wait_for_load_state("networkidle")
    
    print("=== Opening menu ===")
    
    # Click menu button
    menu_btn = page.query_selector('.bm-burger-button')
    if menu_btn:
        page.click('.bm-burger-button')
        page.wait_for_timeout(1000)
        print("Menu clicked")
    
    # Look for logout link
    locators_to_try = [
        '[data-test="logout-sidebar-link"]',
        'text=Logout',
        'button:has-text("Logout")',
        'a:has-text("Logout")',
        '[id="logout_sidebar_link"]'
    ]
    
    print("\n=== Searching for logout ===")
    for locator in locators_to_try:
        elem = page.query_selector(locator)
        if elem:
            print(f"✓ Found: {locator}")
        else:
            print(f"✗ Not found: {locator}")
    
    # Get all menu items
    print("\n=== All menu items ===")
    menu_items = page.query_selector_all('.bm-menu a, .bm-menu button')
    for i, item in enumerate(menu_items):
        text = item.inner_text()
        href = item.get_attribute('href')
        id_attr = item.get_attribute('id')
        print(f"{i}: text='{text}', href='{href}', id='{id_attr}'")
    
    browser.close()
