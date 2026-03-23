"""
Test data constants for Sauce Demo automation tests.
"""

# Valid user credentials
VALID_USERS = {
    "standard": {
        "username": "standard_user",
        "password": "secret_sauce"
    },
    "locked": {
        "username": "locked_out_user",
        "password": "secret_sauce"
    },
    "problem": {
        "username": "problem_user",
        "password": "secret_sauce"
    },
    "performance": {
        "username": "performance_glitch_user",
        "password": "secret_sauce"
    }
}

# Invalid credentials for negative testing
INVALID_CREDENTIALS = [
    {
        "username": "wrong_user",
        "password": "wrong_pass"
    },
    {
        "username": "",
        "password": "secret_sauce"
    },
    {
        "username": "standard_user",
        "password": ""
    },
    {
        "username": "",
        "password": ""
    }
]

# All available products on Sauce Demo
PRODUCTS = [
    "Sauce Labs Backpack",
    "Sauce Labs Bike Light",
    "Sauce Labs Bolt T-Shirt",
    "Sauce Labs Fleece Jacket",
    "Sauce Labs Onesie",
    "Test.allTheThings() T-Shirt (Red)"
]

# Default checkout information
CHECKOUT_INFO = {
    "first_name": "John",
    "last_name": "Doe",
    "zip": "12345"
}

# Error messages
ERROR_MESSAGES = {
    "locked_user": "Epic sadface: Sorry, this user has been locked out.",
    "invalid_credentials": "Epic sadface: Username and password do not match any user in this service"
}

# Page URLs
BASE_URL = "https://www.saucedemo.com"
LOGIN_URL = f"{BASE_URL}/"
INVENTORY_URL = f"{BASE_URL}/inventory.html"
CART_URL = f"{BASE_URL}/cart.html"
CHECKOUT_STEP_ONE_URL = f"{BASE_URL}/checkout-step-one.html"
CHECKOUT_STEP_TWO_URL = f"{BASE_URL}/checkout-step-two.html"
CHECKOUT_COMPLETE_URL = f"{BASE_URL}/checkout-complete.html"
