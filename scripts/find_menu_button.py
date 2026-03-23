"""
Script to find the correct menu button locator on Sauce Demo.
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
    
    print("=== Searching for menu button ===")
    
    # Try different selectors
    locators_to_try = [
        '[data-test="bm-menu-button"]',
        '.bm-menu-button',
        'button.bm-burger-button',
        '.bm-burger-button',
        '[id="menu-button"]',
        '.menu-button',
        'button:has-text("Menu")',
        '[aria-label="Menu"]'
    ]
    
    for locator in locators_to_try:
        elem = page.query_selector(locator)
        if elem:
            print(f"✓ Found: {locator}")
        else:
            print(f"✗ Not found: {locator}")
    
    # Get all buttons on page
    print("\n=== All buttons on page ===")
    buttons = page.query_selector_all('button')
    for i, btn in enumerate(buttons):
        text = btn.inner_text()
        classes = btn.get_attribute('class')
        data_test = btn.get_attribute('data-test')
        print(f"{i}: text='{text}', class='{classes}', data-test='{data_test}'")
    
    # Check for menu elements
    print("\n=== Menu/Burger related elements ===")
    divs = page.query_selector_all('div')
    for div in divs:
        class_attr = div.get_attribute('class')
        id_attr = div.get_attribute('id')
        if class_attr and ('menu' in class_attr.lower() or 'burger' in class_attr.lower()):
            print(f"Found: class='{class_attr}', id='{id_attr}'")
        if id_attr and ('menu' in id_attr.lower() or 'burger' in id_attr.lower()):
            print(f"Found: id='{id_attr}'")
    
    print("\n=== Checking for visible menu button ===")
    # Sometimes the menu button might not have data-test
    import time
    time.sleep(1)
    page.screenshot(path="inventory_page.png")
    print("Screenshot saved as inventory_page.png")
    
    browser.close()
