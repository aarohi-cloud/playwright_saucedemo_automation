# Sauce Demo Automation Framework

**Advanced E2E Test Automation for SauceDemo.com using Playwright & Pytest**

A production-ready test automation framework built with **Python 3.13**, **Playwright**, and **Pytest**, implementing the **Page Object Model (POM)** pattern with a shared `BasePage`, comprehensive test coverage, auto-retry on flakiness, email reporting, pre-commit hooks, and CI/CD integration.

---

## Table of Contents

1. [Project Overview](#project-overview)
2. [Tech Stack](#tech-stack)
3. [Prerequisites](#prerequisites)
4. [Setup Instructions](#setup-instructions)
5. [Running Tests](#running-tests)
6. [Viewing Reports](#viewing-reports)
7. [Project Structure](#project-structure)
8. [Test Cases Summary](#test-cases-summary)
9. [Email Reporting](#email-reporting)
10. [Pre-commit Hooks](#pre-commit-hooks)
11. [Known Issues & Limitations](#known-issues--limitations)
12. [Quick Reference](#quick-reference)
13. [CI/CD Integration](#cicd-integration)
14. [Contributing](#contributing)

---

## Project Overview

This automation framework tests the complete user journey on **https://www.saucedemo.com/**, including:

- **User Authentication** — Login with various user types and credentials
- **Product Discovery** — Browse, search, and sort products
- **Shopping Cart** — Add/remove items, view cart, manage quantities
- **Checkout Process** — Complete purchase flow with validation
- **Error Handling** — Edge cases, negative tests, form validation

### What It Tests

- **Authentication (8 tests)** — Valid login, locked accounts, invalid credentials, empty fields
- **Inventory (7 tests)** — Product display, sorting (A-Z, Z-A, price), product details
- **Cart (8 tests)** — Add items, remove items, persistence, badge updates
- **Checkout (7 tests)** — Complete flow, validation, cancellation, order totals

**Total: 30 tests across 4 modules**
**Coverage: 100% of critical user workflows**
**Browsers verified: Chromium, Firefox — 30/30 passed on both**

---

## Tech Stack

| Component | Technology | Version |
|-----------|-----------|---------|
| **Language** | Python | 3.13.7 |
| **Testing Framework** | Pytest | 9.0.2 |
| **Browser Automation** | Playwright | 1.58.0 |
| **Design Pattern** | Page Object Model (POM) + BasePage | — |
| **Reporting** | pytest-html + Allure | 4.2.0 + 2.15.3 |
| **Parallel Execution** | pytest-xdist | — |
| **Auto-retry on Flakiness** | pytest-rerunfailures | 16.1 |
| **Env Var Management** | python-dotenv | 1.2.2 |
| **Code Quality** | black + flake8 + pre-commit | — |
| **Environment** | Virtual Environment (.venv) | Python 3.13 |

### Why These Technologies?

- **Playwright** — Modern browser automation with Chromium, Firefox, WebKit support
- **BasePage** — Shared `safe_fill`, `safe_click`, `safe_select`, `retry_action` helpers eliminate duplication across all page objects
- **pytest-rerunfailures** — Automatically re-runs flaky tests once before marking them failed
- **python-dotenv** — Loads `.env` for local dev; CI injects real env vars directly
- **pre-commit + black + flake8** — Enforces consistent formatting and catches issues before commit

---

## Prerequisites

- **Python 3.11+** (project uses 3.13.7)
- **pip** (comes with Python)
- **Git**
- **Node.js 18+** (required by Playwright browser installer)

### Verification Commands

```bash
python --version
pip --version
git --version
```

---

## Setup Instructions

### Step 1: Clone the Repository

```bash
git clone <repository-url>
cd saucedemo_automation
```

### Step 2: Create and Activate Virtual Environment

**Windows (PowerShell):**
```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
# If blocked by execution policy:
# Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

**macOS/Linux:**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Install Playwright Browsers

```bash
# Chromium only (fastest)
playwright install chromium

# Both Chromium and Firefox (used in CI)
playwright install chromium firefox
```

### Step 5: Configure Environment (Optional — for email reporting)

```bash
# Copy the example file and fill in your values
cp .env.example .env
# Edit .env and set EMAIL_ENABLED=true plus SMTP settings
```

### Verification

```bash
python -c "from playwright.sync_api import sync_playwright; print('Playwright ready')"
pytest --version
```

---

## Running Tests

### Run All Tests

```bash
# Run all 30 tests (Chromium, default)
pytest

# Run with explicit browser
pytest --browser=chromium -v
pytest --browser=firefox -v
```

### Run Specific Test File

```bash
pytest tests/test_login.py -v
pytest tests/test_inventory.py -v
pytest tests/test_cart.py -v
pytest tests/test_checkout.py -v
```

### Run by Marker

```bash
# Smoke tests only (6 critical tests, ~31 seconds)
pytest -m smoke -v

# Regression tests only (24 tests)
pytest -m regression -v

# By module
pytest -m login -v        # 8 tests
pytest -m inventory -v    # 7 tests
pytest -m cart -v         # 8 tests
pytest -m checkout -v     # 7 tests

# Combined markers
pytest -m "smoke and login" -v
pytest -m "regression and cart" -v
```

### Multi-Browser

```bash
# Run on Chromium and Firefox together
pytest --browser=chromium --browser=firefox -v
```

### Parallel Execution

```bash
# 4 workers (4x faster)
pytest -n 4 -v

# Auto-detect CPU cores
pytest -n auto -v
```

### Debug a Specific Test

```bash
# Single test with stdout
pytest tests/test_login.py::test_valid_login_standard_user -v -s

# Stop on first failure
pytest -x -v

# Re-run only last failed tests
pytest --lf -v

# Show 10 slowest tests
pytest --durations=10 -v
```

---

## Viewing Reports

### HTML Report

Generated automatically after every run at `reports/report.html`.

```powershell
# Windows
start reports/report.html
```
```bash
# macOS
open reports/report.html

# Linux
xdg-open reports/report.html
```

### JUnit XML Report

Generated at `reports/junit-report.xml` after every run — consumed by GitHub Actions, Jenkins, and other CI tools automatically.

### Allure Report (Interactive Dashboard)

```bash
# Run and collect Allure data
pytest --alluredir=allure-results -v

# Generate and serve report
allure generate allure-results --clean -o allure-report
allure serve allure-results
```

Report opens at `http://localhost:4040`.

---

## Project Structure

```
saucedemo_automation/
│
├── pages/                          # Page Object Model classes
│   ├── __init__.py
│   ├── base_page.py                # BasePage — shared helpers for all page objects
│   ├── login_page.py               # Login page (inherits BasePage)
│   ├── inventory_page.py           # Product listing page (inherits BasePage)
│   ├── cart_page.py                # Shopping cart page (inherits BasePage)
│   ├── checkout_page.py            # Checkout flow pages (inherits BasePage)
│   └── product_detail_page.py      # Product detail view (inherits BasePage)
│
├── tests/                          # Test files (30 tests total)
│   ├── __init__.py
│   ├── test_login.py               # 8 authentication tests
│   ├── test_inventory.py           # 7 product discovery tests
│   ├── test_cart.py                # 8 cart management tests
│   ├── test_checkout.py            # 7 purchase flow tests
│   └── utils/
│       ├── __init__.py
│       ├── test_data.py            # Test data, credentials, products
│       └── helpers.py              # Reusable helper functions
│
├── utils/
│   ├── locators.json               # Element locators reference
│   └── email_reporter.py           # Post-run email notification (opt-in via .env)
│
├── docs/                           # Documentation
│   ├── INDEX.md
│   ├── TEST_CASE_MATRIX.md
│   ├── TEST_COMMANDS.md
│   ├── TEST_EXECUTION_FLOW.md
│   └── TEST_EXECUTION_REPORT.md
│
├── scripts/                        # Debug/utility scripts
│   ├── find_logout.py
│   ├── find_menu_button.py
│   └── inspect_locators.py
│
├── assets/
│   └── inventory_page.png
│
├── reports/                        # Generated after each run (git-ignored)
│   ├── report.html                 # HTML report
│   └── junit-report.xml            # JUnit XML report
│
├── allure-results/                 # Allure raw data (git-ignored)
├── allure-report/                  # Allure generated report (git-ignored)
│
├── .github/workflows/
│   └── playwright-tests.yml        # GitHub Actions CI workflow
│
├── conftest.py                     # Session hooks: screenshot-on-failure, email report
├── pytest.ini                      # Pytest config: options, markers, reruns
├── requirements.txt                # Python dependencies
├── .env.example                    # Email config template (copy to .env)
├── .pre-commit-config.yaml         # black + flake8 pre-commit hooks
├── .gitignore
└── README.md
```

### Key Files

| File | Purpose |
|------|---------|
| `pages/base_page.py` | `BasePage` with `safe_fill`, `safe_click`, `safe_select`, `navigate_to`, `retry_action` |
| `conftest.py` | Allure screenshot hook on failure + post-session email hook |
| `pytest.ini` | `--reruns 1`, `--reruns-delay 2`, `--junitxml`, Allure, HTML options |
| `utils/email_reporter.py` | Sends HTML+XML zip via SMTP when `EMAIL_ENABLED=true` |
| `.env.example` | Template for SMTP credentials — copy to `.env`, never commit |
| `.pre-commit-config.yaml` | Runs `black`, `flake8`, and safety checks before each commit |
| `tests/utils/test_data.py` | Credentials, product names, checkout info |
| `tests/utils/helpers.py` | `login_as()`, `add_products_to_cart()`, `complete_checkout()` |

---

## Test Cases Summary

### LOGIN TESTS (8 tests) — `test_login.py`

| # | Test Name | Type | Purpose |
|---|-----------|------|---------|
| 1 | `test_valid_login_standard_user` | Smoke | Valid user can login |
| 2 | `test_locked_out_user` | Regression | Locked account shows error |
| 3 | `test_invalid_username` | Regression | Invalid username validation |
| 4 | `test_invalid_password` | Regression | Invalid password validation |
| 5 | `test_empty_username` | Regression | Empty username validation |
| 6 | `test_empty_password` | Regression | Empty password validation |
| 7 | `test_both_fields_empty` | Regression | Both fields empty validation |
| 8 | `test_logout` | Smoke | User can logout successfully |

### INVENTORY TESTS (7 tests) — `test_inventory.py`

| # | Test Name | Type | Purpose |
|---|-----------|------|---------|
| 1 | `test_inventory_page_loads` | Smoke | All 6 products display |
| 2 | `test_sort_products_az` | Regression | A-Z sorting works |
| 3 | `test_sort_products_za` | Regression | Z-A sorting works |
| 4 | `test_sort_by_price_low_high` | Regression | Price low-high sorting |
| 5 | `test_sort_by_price_high_low` | Regression | Price high-low sorting |
| 6 | `test_product_detail_page` | Regression | Product detail loads |
| 7 | `test_add_product_from_detail_page` | Regression | Add from detail page |

### CART TESTS (8 tests) — `test_cart.py`

| # | Test Name | Type | Purpose |
|---|-----------|------|---------|
| 1 | `test_add_single_item_to_cart` | Smoke | Add 1 item |
| 2 | `test_add_multiple_items_to_cart` | Smoke | Add 3 items |
| 3 | `test_remove_item_from_cart` | Regression | Remove item |
| 4 | `test_cart_persists_after_navigation` | Regression | Cart persists across pages |
| 5 | `test_cart_item_details` | Regression | Item details display correctly |
| 6 | `test_continue_shopping` | Regression | Continue shopping button works |
| 7 | `test_cart_badge_updates` | Regression | Badge count updates |
| 8 | `test_remove_all_items` | Regression | Remove all items |

### CHECKOUT TESTS (7 tests) — `test_checkout.py`

| # | Test Name | Type | Purpose |
|---|-----------|------|---------|
| 1 | `test_complete_checkout_flow` | Smoke | Complete E2E purchase |
| 2 | `test_checkout_without_items` | Regression | Empty cart behavior |
| 3 | `test_missing_first_name` | Regression | First name validation |
| 4 | `test_missing_last_name` | Regression | Last name validation |
| 5 | `test_missing_zip_code` | Regression | Zip code validation |
| 6 | `test_verify_order_total` | Regression | Order total calculation |
| 7 | `test_checkout_cancel` | Regression | Cancel checkout |

### Test Summary

```
Total Tests:          30
├─ Smoke (Critical):  6  (20%)
└─ Regression:       24  (80%)

By Module:
├─ Login:            8 tests
├─ Inventory:        7 tests
├─ Cart:             8 tests
└─ Checkout:         7 tests

Execution Times (verified):
├─ Chromium (full):  ~145 seconds (2:25)
├─ Firefox (full):   ~184 seconds (3:04)
├─ Smoke only:       ~31 seconds
└─ Parallel (4x):    ~40 seconds (estimate)

Results:
└─ 30/30 passed on Chromium  ✅
└─ 30/30 passed on Firefox   ✅
```

---

## Email Reporting

After a test run completes, the framework can automatically email a summary with the HTML and JUnit reports attached.

### Setup

```bash
# Copy the template
cp .env.example .env
```

Edit `.env`:

```env
EMAIL_ENABLED=true
EMAIL_TO=you@example.com
EMAIL_FROM=your-smtp@example.com
EMAIL_SUBJECT_PREFIX=SauceDemo Tests
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=your-smtp@example.com
SMTP_PASSWORD=your-app-password
EMAIL_USE_TLS=true
```

### What the email contains

- Pass / fail / skip counts
- Exit status code
- Names of up to 5 failing tests
- Zip attachment of `reports/report.html` and `reports/junit-report.xml`

> **Note:** `.env` is git-ignored. Never commit it. Use `.env.example` as the committed template.

---

## Pre-commit Hooks

The repo ships with a `.pre-commit-config.yaml` that runs **black**, **flake8**, and standard safety checks on every `git commit`.

### Install hooks (one-time)

```bash
pip install pre-commit
pre-commit install
```

### Hooks configured

| Hook | Tool | What it does |
|------|------|-------------|
| `trailing-whitespace` | pre-commit | Strips trailing spaces |
| `end-of-file-fixer` | pre-commit | Ensures files end with a newline |
| `check-yaml` | pre-commit | Validates YAML syntax |
| `check-merge-conflict` | pre-commit | Blocks leftover merge markers |
| `debug-statements` | pre-commit | Blocks `import pdb`, `breakpoint()` |
| `black` | black 23.12.1 | Auto-formats Python to PEP 8 |
| `flake8` | flake8 7.0.0 | Lints Python (max-line=100) |

### Run manually

```bash
# Run all hooks on staged files
pre-commit run

# Run all hooks on every file in the repo
pre-commit run --all-files
```

---

## Known Issues & Limitations

### Issue 1: Playwright Browser Not Found

```
Error: Executable doesn't exist at /path/to/chromium
```

**Fix:**
```bash
playwright install chromium
```

---

### Issue 2: Timeout Error

```
Timeout: Page.click: Timeout waiting for element selector
```

**Causes:** Page didn't load, selector changed, or network latency.

**Fix:** The framework auto-retries once (`--reruns 1 --reruns-delay 2`). If it fails twice, run the test in headed mode to see what's happening:

```bash
pytest tests/test_login.py::test_logout --browser=chromium --headed -v -s
```

---

### Issue 3: `fixture 'page' not found`

```
fixture 'page' not found
```

**Fix:**
```bash
# Activate virtual environment first
.venv\Scripts\Activate.ps1   # Windows
source .venv/bin/activate    # macOS/Linux

pip install -r requirements.txt
pytest tests/
```

---

### Issue 4: HTML Report Not Generated

```
reports/report.html not found
```

**Fix:**
```bash
mkdir reports
pytest tests/ -v
```

---

### Remaining Limitations

| Limitation | Impact | Status |
|-----------|--------|--------|
| Test data hardcoded | Fixed user set | Low — covers all SauceDemo user types |
| No WebKit testing | Safari not verified | Can add `--browser=webkit` |
| No API integration | Backend not verified | Scope is UI tests only |
| Email requires SMTP | Needs valid credentials | Optional feature, off by default |

---

## Quick Reference

### Most Common Commands

```bash
# Run all tests
pytest -v

# Smoke tests only
pytest -m smoke -v

# Specific browser
pytest --browser=chromium -v
pytest --browser=firefox -v

# Run on both browsers
pytest --browser=chromium --browser=firefox -v

# Parallel execution
pytest -n 4 -v

# Run specific file
pytest tests/test_login.py -v

# Debug failing test
pytest tests/test_login.py::test_logout -v -s --headed

# Re-run last failures
pytest --lf -v

# Show slowest tests
pytest --durations=10 -v
```

### Report Locations

```
reports/
├── report.html          # Open in browser after each run
└── junit-report.xml     # Consumed by CI (GitHub Actions, Jenkins)

allure-results/          # Raw Allure data (run: allure serve allure-results)
allure-report/           # Generated Allure HTML dashboard
```

---

## CI/CD Integration

The framework ships with a GitHub Actions workflow at [.github/workflows/playwright-tests.yml](.github/workflows/playwright-tests.yml).

### What the workflow does

- Triggers on every push and pull request to `main`
- Installs Python 3.13 and all dependencies
- Installs Chromium via `playwright install chromium`
- Runs the full 30-test suite
- Uploads `reports/` as a build artifact on every run (pass or fail)
- JUnit XML is parsed by GitHub Actions to display inline test results

### GitHub Actions snippet

```yaml
name: Playwright Tests
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.13'
      - run: pip install -r requirements.txt
      - run: playwright install chromium
      - run: pytest --browser=chromium -v --tb=short
      - uses: actions/upload-artifact@v4
        if: always()
        with:
          name: test-reports
          path: reports/
```

---

## Contributing

1. **Create a feature branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Install pre-commit hooks** (first time only)
   ```bash
   pip install pre-commit
   pre-commit install
   ```

3. **Run tests before pushing**
   ```bash
   pytest -m smoke -v          # Quick sanity check
   pytest --browser=chromium   # Full suite
   ```

4. **Rules**
   - Never modify files inside `tests/` — only page objects and config
   - Keep all public method names in page objects identical (tests depend on them)
   - New page interactions go in the relevant `pages/*.py` class
   - New test data goes in `tests/utils/test_data.py`
   - Follow PEP 8 — black will enforce it on commit

5. **Commit and push**
   ```bash
   git add pages/
   git commit -m "feat: describe your change"
   git push origin feature/your-feature-name
   ```

---

## Project Statistics

| Metric | Value |
|--------|-------|
| **Total Tests** | 30 |
| **Test Files** | 4 |
| **Page Objects** | 5 (+ 1 BasePage) |
| **Helper Functions** | 3 (`login_as`, `add_products_to_cart`, `complete_checkout`) |
| **Smoke Tests** | 6 (20%) |
| **Regression Tests** | 24 (80%) |
| **Browsers Verified** | Chromium, Firefox |
| **Chromium Runtime** | ~145 seconds (2:25) |
| **Firefox Runtime** | ~184 seconds (3:04) |
| **Smoke Runtime** | ~31 seconds |
| **Auto-retry** | 1 rerun on failure, 2s delay |
| **Coverage** | 100% of critical workflows |

---

## Status

```
PROJECT STATUS: PRODUCTION READY

All 30 tests passing on Chromium  ✅
All 30 tests passing on Firefox   ✅
BasePage with safe helpers        ✅
Auto-retry on flakiness           ✅
Allure screenshot on failure      ✅
JUnit XML for CI                  ✅
Email reporting (opt-in)          ✅
pre-commit hooks (black/flake8)   ✅
GitHub Actions CI                 ✅
.env.example for secrets          ✅

Last Updated: March 27, 2026
Framework Version: 2.0
```

---

**Ready to start? Jump to [Setup Instructions](#setup-instructions) or run `pytest -m smoke -v` for a 31-second sanity check.**
