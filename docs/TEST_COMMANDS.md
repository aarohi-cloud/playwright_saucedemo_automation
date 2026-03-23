# TEST COMMANDS REFERENCE - Sauce Demo Automation Framework

**Framework:** Pytest + Playwright  
**Project:** SauceDemo E2E Automation  
**Test Files:** 4 modules (30 tests total)  
**Location:** `tests/`  
**Config:** `pytest.ini`  

---

## Table of Contents
1. [Quick Start](#quick-start)
2. [Combined Marker Runs](#combined-marker-runs)
3. [Test Reports](#test-reports)
4. [Parallel Execution](#parallel-execution)
5. [Test Discovery](#test-discovery)
6. [Single & Multi-Test Execution](#single--multi-test-execution)
7. [Debug Mode](#debug-mode)
8. [Test Filtering by Keyword](#test-filtering-by-keyword)
9. [Performance Commands](#performance-commands)
10. [Output Options](#output-options)
11. [Markers Reference](#markers-reference)
12. [Recommended Runs](#recommended-runs)
13. [Configuration](#configuration)
14. [Docker Execution](#docker-execution)
15. [Important Notes & Tips](#important-notes--tips)

---

## 1. Quick Start

### Run All Tests (Full Suite - 30 tests)

```bash
# Run all tests with default output
pytest tests/

# Run all tests with verbose output
pytest tests/ -v

# Run all tests with reports (HTML + Allure)
pytest tests/ -v --html=reports/report.html --alluredir=reports/allure
```

### Run by Test File

```bash
# Run login tests only (8 tests)
pytest tests/test_login.py -v

# Run inventory tests only (7 tests)
pytest tests/test_inventory.py -v

# Run cart tests only (8 tests)
pytest tests/test_cart.py -v

# Run checkout tests only (7 tests)
pytest tests/test_checkout.py -v

# Run multiple specific files
pytest tests/test_login.py tests/test_cart.py -v
```

### Run by Marker/Tag

```bash
# Run smoke tests only (6 critical tests, ~20 seconds)
pytest tests/ -m smoke -v

# Run regression tests only (24 detailed tests, ~108 seconds)
pytest tests/ -m regression -v

# Run login module tests (8 tests)
pytest tests/ -m login -v

# Run inventory module tests (7 tests)
pytest tests/ -m inventory -v

# Run cart module tests (8 tests)
pytest tests/ -m cart -v

# Run checkout module tests (7 tests)
pytest tests/ -m checkout -v
```

---

## 2. Combined Marker Runs

### AND Operations (Tests must match ALL markers)

```bash
# Run tests that are BOTH smoke AND login (@smoke AND @login)
pytest tests/ -m "smoke and login" -v

# Run tests that are BOTH regression AND cart (@regression AND @cart)
pytest tests/ -m "regression and cart" -v

# Run tests that are smoke AND (login OR checkout)
pytest tests/ -m "smoke and (login or checkout)" -v

# Run tests that are regression AND NOT checkout
pytest tests/ -m "regression and not checkout" -v
```

### OR Operations (Tests match ANY marker)

```bash
# Run tests that are smoke OR regression (same as all tests)
pytest tests/ -m "smoke or regression" -v

# Run tests from login OR cart modules
pytest tests/ -m "login or cart" -v

# Run tests from any module except checkout
pytest tests/ -m "login or cart or inventory" -v
```

### Complex Marker Combinations

```bash
# Run all high-priority tests: smoke from any module or critical regression
pytest tests/ -m "smoke or (regression and (login or checkout))" -v

# Run smoke tests from login and cart, plus all checkout regression
pytest tests/ -m "(smoke and (login or cart)) or (regression and checkout)" -v

# Run all tests EXCEPT low-priority ones (if tagged)
pytest tests/ -m "smoke or regression" -v
```

---

## 3. Test Reports

### HTML Report Generation

```bash
# Generate basic HTML report
pytest tests/ --html=reports/report.html -v

# Generate self-contained HTML (CSS/JS embedded, one file)
pytest tests/ --html=reports/report.html --self-contained-html -v

# Open HTML report after tests (macOS)
pytest tests/ --html=reports/report.html && open reports/report.html

# Open HTML report after tests (Windows)
pytest tests/ --html=reports/report.html && start reports/report.html

# Open HTML report after tests (Linux)
pytest tests/ --html=reports/report.html && xdg-open reports/report.html
```

### Allure Report Generation

```bash
# Generate Allure report data
pytest tests/ --alluredir=reports/allure -v

# Generate Allure report and serve it (requires: pip install allure-pytest)
pytest tests/ --alluredir=reports/allure && allure serve reports/allure

# Generate both HTML and Allure reports
pytest tests/ -v --html=reports/report.html --self-contained-html --alluredir=reports/allure

# Clear old allure data and generate fresh
rm -rf reports/allure
pytest tests/ --alluredir=reports/allure -v
```

### JUnit XML Report

```bash
# Generate JUnit XML (for CI/CD integration)
pytest tests/ --junit-xml=reports/junit.xml -v

# Generate all three report types together
pytest tests/ -v \
  --html=reports/report.html --self-contained-html \
  --alluredir=reports/allure \
  --junit-xml=reports/junit.xml
```

### Report Output Control

```bash
# Generate report with custom title
pytest tests/ --html=reports/report.html --self-contained-html \
  --html-report=reports/report.html -v

# Save test logs to file
pytest tests/ -v > reports/test_logs.txt 2>&1

# Save logs with pipe (Windows)
pytest tests/ -v | Tee-Object -FilePath reports/test_logs.txt
```

---

## 4. Parallel Execution

### Fixed Number of Workers

```bash
# Run with 2 workers (requires: pip install pytest-xdist)
pytest tests/ -n 2 -v

# Run with 4 workers (4x speedup)
pytest tests/ -n 4 -v

# Run with 8 workers (max parallelization)
pytest tests/ -n 8 -v

# Run with 4 workers and distribute by test scope
pytest tests/ -n 4 --dist loadscope -v

# Run with 4 workers and show individual worker output
pytest tests/ -n 4 -v
```

### Auto-Detect Workers

```bash
# Use all available CPU cores
pytest tests/ -n auto -v

# Use auto-detected cores with load scope distribution
pytest tests/ -n auto --dist loadscope -v
```

### Parallel with Specific Groups

```bash
# Run smoke tests in parallel (4 workers)
pytest tests/ -m smoke -n 4 -v

# Run by module with parallelization
pytest tests/test_cart.py -n 4 -v

# Parallel with HTML reporting
pytest tests/ -n 4 --html=reports/report.html --self-contained-html -v
```

### Run Sequentially (Default)

```bash
# Run without parallelization (standard sequential)
pytest tests/ -v

# Explicitly force sequential (single worker)
pytest tests/ -n 0 -v
```

---

## 5. Test Discovery

### List All Tests

```bash
# Show all tests that will run
pytest tests/ --collect-only

# Show test count summary
pytest tests/ --collect-only -q

# Collect tests and format output
pytest tests/ --collect-only --quiet

# Show tests with their markers
pytest tests/ --collect-only -q | grep -E "(test_|MARKER)"

# Export test list to file
pytest tests/ --collect-only -q > reports/test_list.txt
```

### List Tests by Marker

```bash
# List all smoke tests
pytest tests/ -m smoke --collect-only -q

# List all regression tests
pytest tests/ -m regression --collect-only -q

# List tests by module
pytest tests/ -m login --collect-only -q
pytest tests/ -m inventory --collect-only -q
pytest tests/ -m cart --collect-only -q
pytest tests/ -m checkout --collect-only -q

# List all markers available
pytest tests/ --markers
```

### Test Count Verification

```bash
# Count total tests and show summary
pytest tests/ --collect-only | grep "test session starts" -A 5

# Quick count of tests
pytest tests/ --collect-only -q | wc -l

# List with line numbers
pytest tests/ --collect-only -q | nl
```

---

## 6. Single & Multi-Test Execution

### Run Single Specific Test

```bash
# Run one test by full path
pytest tests/test_login.py::test_valid_login_standard_user -v

# Run one test by module and name
pytest tests/test_cart.py::test_add_single_item_to_cart -v

# Run one test by shortest unique name
pytest test_logout -v
```

### Run Multiple Specific Tests

```bash
# Run two specific tests
pytest tests/test_login.py::test_valid_login_standard_user tests/test_logout -v

# Run all tests in a class (if organized by class)
pytest tests/test_login.py::TestLogin -v

# Run multiple tests from different files
pytest \
  tests/test_login.py::test_valid_login_standard_user \
  tests/test_cart.py::test_add_single_item_to_cart \
  tests/test_checkout.py::test_complete_checkout_flow \
  -v
```

### Run Tests by Partial Name

```bash
# Run all tests containing "login" in name
pytest tests/ -k "login" -v

# Run all tests starting with "test_add"
pytest tests/ -k "add" -v

# Run all tests NOT containing "logout"
pytest tests/ -k "not logout" -v

# Run tests with complex keyword patterns
pytest tests/ -k "login and not logout" -v
```

---

## 7. Debug Mode

### Verbose & Print Output

```bash
# Show print statements and detailed output (-s = capture output)
pytest tests/ -v -s

# Verbose with local variables on failure
pytest tests/ -v -l

# Ultra verbose with full print statements
pytest tests/ -vv -s

# Show captured output even on passed tests
pytest tests/ -s -v --tb=short
```

### Stop on First Failure

```bash
# Stop after first test failure (fail-fast)
pytest tests/ -x -v

# Stop after first 3 failures
pytest tests/ -x --maxfail=3 -v

# Stop after first failure and show local variables
pytest tests/ -x -l -v
```

### Last Failed Tests

```bash
# Run only tests that failed in the last run
pytest tests/ --lf -v

# Run failed tests first, then pass others
pytest tests/ --ff -v

# Run failed tests with verbose output
pytest tests/ --lf -v -s
```

### Debugging with PDB (Python Debugger)

```bash
# Drop to debugger on failure
pytest tests/ --pdb -v

# Drop to debugger on first failure and always
pytest tests/ --pdb -x -v

# Drop to debugger on failures in specific test
pytest tests/test_login.py::test_valid_login_standard_user --pdb -v

# Show local variables at breakpoint
pytest tests/ --pdb -l
```

### Traceback Control

```bash
# Short traceback format
pytest tests/ --tb=short -v

# Long traceback format
pytest tests/ --tb=long -v

# No traceback (just pass/fail)
pytest tests/ --tb=no -v

# Line-by-line traceback
pytest tests/ --tb=line -v

# Show locals in traceback
pytest tests/ --tb=short -l -v
```

---

## 8. Test Filtering by Keyword

### Keyword Pattern Matching

```bash
# Run tests matching keyword "checkout"
pytest tests/ -k "checkout" -v

# Run tests matching "test_add"
pytest tests/ -k "test_add" -v

# Run tests NOT matching "empty" (negative match)
pytest tests/ -k "not empty" -v

# Run tests with multiple keywords (AND)
pytest tests/ -k "cart and not remove" -v

# Run tests with keyword alternatives (OR)
pytest tests/ -k "login or logout" -v
```

### Complex Filtering Patterns

```bash
# Run smoke tests containing "checkout"
pytest tests/ -m smoke -k "checkout" -v

# Run regression tests NOT in login module
pytest tests/ -m regression -k "not login" -v

# Run tests matching multiple conditions
pytest tests/ -k "(login or logout) and not empty" -v

# Run all cart and checkout tests
pytest tests/ -k "cart or checkout" -v
```

### Case-Sensitive Keyword Matching

```bash
# Case-insensitive (default)
pytest tests/ -k "login" -v

# Match exact test name pattern
pytest tests/ -k "test_valid_login_standard_user" -v

# Run tests with pattern in filename
pytest tests/test_login.py -k "invalid" -v
```

---

## 9. Performance Commands

### Show Slowest Tests

```bash
# Show top 10 slowest tests
pytest tests/ -v --durations=10

# Show all test durations sorted
pytest tests/ -v --durations=0

# Show top 5 slowest tests
pytest tests/ -v --durations=5

# Show tests sorted by duration (slowest first)
pytest tests/ --durations=20 -v
```

### Performance Analysis

```bash
# Run tests and show timing summary
pytest tests/ -v --tb=short --durations=10

# Profile slow tests with timing
pytest tests/ -v -x --durations=0 2>&1 | tail -20

# Time specific slow test in isolation
pytest tests/test_checkout.py::test_complete_checkout_flow -v --durations=0

# Compare timing: smoke vs regression
pytest tests/ -m smoke -v --durations=5
pytest tests/ -m regression -v --durations=5
```

### Measure Full Suite Duration

```bash
# Run full suite and show total time
pytest tests/ -v --tb=short | tail -5

# Run with timer (show start/end time)
echo "START: $(date)" && pytest tests/ -v && echo "END: $(date)"

# Run and save duration to file
pytest tests/ -v > reports/test_run.txt 2>&1 && \
  echo "Tests completed at $(date)" >> reports/test_run.txt
```

---

## 10. Output Options

### Minimal Output

```bash
# Quiet mode (minimal output)
pytest tests/ -q

# Very minimal (dot per test)
pytest tests/ --tb=no -q

# No output except summary
pytest tests/ -q --tb=no
```

### Detailed Output

```bash
# Verbose (default detailed)
pytest tests/ -v

# Ultra verbose
pytest tests/ -vv

# Show variables (verbose with locals)
pytest tests/ -v -l

# Detailed with print output
pytest tests/ -v -s
```

### Color & Formatting

```bash
# Force color output (even in pipes)
pytest tests/ -v --color=yes

# Disable color output
pytest tests/ -v --color=no

# Auto-detect color (default)
pytest tests/ -v --color=auto

# Unicode output (helpful for special characters)
pytest tests/ -v --unicode
```

### Output to Files

```bash
# Redirect all output to file
pytest tests/ -v > reports/output.txt 2>&1

# Redirect with timestamp
pytest tests/ -v > reports/output_$(date +%Y%m%d_%H%M%S).txt 2>&1

# Append to existing log file
pytest tests/ -v >> reports/test_history.log 2>&1

# Tee to both screen and file (Unix)
pytest tests/ -v | tee reports/output.txt

# Tee to both screen and file (PowerShell Windows)
pytest tests/ -v | Tee-Object -FilePath reports/output.txt -Append
```

---

## 11. Markers Reference

### Available Markers in Project

| Marker | Count | Purpose | Usage |
|--------|-------|---------|-------|
| `@smoke` | 6 | Happy path, critical flows | Pre-commit gate, quick validation |
| `@regression` | 24 | Edge cases, detailed validation | Full suite, nightly builds |
| `@login` | 8 | Authentication & authorization | Auth feature validation |
| `@inventory` | 7 | Product display & sorting | Product feature validation |
| `@cart` | 8 | Add/remove items, persistence | Cart feature validation |
| `@checkout` | 7 | Purchase flow, validation | Checkout feature validation |

### Marker Distribution

```
┌──────────────┬───────┬──────────────────────────────────┐
│ Marker       │ Count │ Tests                            │
├──────────────┼───────┼──────────────────────────────────┤
│ smoke        │ 6     │ 20% of all tests (critical)     │
│ regression   │ 24    │ 80% of all tests (comprehensive)│
│ login        │ 8     │ 27% (auth module)               │
│ inventory    │ 7     │ 23% (product module)            │
│ cart         │ 8     │ 27% (cart module)               │
│ checkout     │ 7     │ 23% (purchase module)           │
│ TOTAL        │ 30    │ 100%                            │
└──────────────┴───────┴──────────────────────────────────┘
```

### Marker Usage Examples

```bash
# Run all tests with specific marker
pytest tests/ -m <marker_name> -v

# Combine markers with logical operators
pytest tests/ -m "marker1 and marker2" -v
pytest tests/ -m "marker1 or marker2" -v
pytest tests/ -m "not marker1" -v

# Example real commands
pytest tests/ -m "smoke"                          # 6 tests
pytest tests/ -m "regression"                     # 24 tests
pytest tests/ -m "smoke and login"                # ~2 tests
pytest tests/ -m "regression and cart"            # ~6 tests
pytest tests/ -m "login or checkout"              # 15 tests
pytest tests/ -m "not login"                      # 22 tests
```

---

## 12. Recommended Runs

### For CI/CD Pipeline

```bash
# Pre-commit hook (smoke tests only - gates commit)
pytest tests/ -m smoke -v --tb=short

# Pull request validation (full regression)
pytest tests/ -v --html=reports/report.html --self-contained-html \
  --alluredir=reports/allure --junit-xml=reports/junit.xml

# Nightly build (everything with reports)
pytest tests/ -n 4 -v --html=reports/report.html --self-contained-html \
  --alluredir=reports/allure --junit-xml=reports/junit.xml

# Production deployment gate (smoke only)
pytest tests/ -m smoke -v --tb=short --junit-xml=reports/junit.xml
```

### For Local Development

```bash
# Quick sanity check (smoke tests)
pytest tests/ -m smoke -v

# Single module debugging
pytest tests/test_login.py -v -s

# Run failed tests only (iterative fixing)
pytest tests/ --lf -v -s

# Run with debug on failure
pytest tests/ -x --pdb -v

# Fast iteration (stop on first fail)
pytest tests/ -x -v
```

### For Performance Testing

```bash
# Show which tests are slowest
pytest tests/ -v --durations=10

# Run in parallel and compare timing
pytest tests/ -n 4 -v --durations=5

# Baseline performance run (save for comparison)
pytest tests/ -v > reports/baseline_$(date +%Y%m%d).txt

# Track performance regression
pytest tests/ -v --durations=20 > reports/latest_run.txt
diff reports/baseline_*.txt reports/latest_run.txt
```

### By Testing Phase

```bash
# PHASE 1: Pre-commit (developers)
pytest tests/ -m smoke -x -v

# PHASE 2: PR submission (validate one module)
pytest tests/test_login.py -v --html=reports/report.html

# PHASE 3: Integration (smoke + one regression module)
pytest tests/ -m "smoke or login" -v --html=reports/report.html

# PHASE 4: Full regression (before release)
pytest tests/ -v --html=reports/report.html --alluredir=reports/allure

# PHASE 5: Parallel full suite (final validation)
pytest tests/ -n 4 -v --html=reports/report.html --alluredir=reports/allure
```

---

## 13. Configuration

### Current pytest.ini Configuration

```ini
[pytest]
testpaths = tests
addopts = --html=reports/report.html --self-contained-html --alluredir=reports/allure -v
markers =
    smoke: marks tests as smoke tests
    regression: marks tests as regression tests
    login: marks tests as login tests
    cart: marks tests as cart tests
    checkout: marks tests as checkout tests
    inventory: marks tests as inventory tests
```

### Key Configuration Details

| Setting | Value | Purpose |
|---------|-------|---------|
| `testpaths` | `tests` | Directory where pytest looks for tests |
| `addopts` | Default options | Automatically applied to every pytest run |
| `--html` | `reports/report.html` | Save HTML report to this location |
| `--self-contained-html` | Enabled | Embed CSS/JS in single HTML file |
| `--alluredir` | `reports/allure` | Allure report data directory |
| `-v` | Verbose | Show detailed test output by default |

### Modify Configuration Temporarily

```bash
# Override testpaths
pytest tests/test_login.py -v

# Disable HTML report generation (override addopts)
pytest tests/ -v -p no:html

# Skip Allure report (remove from addopts)
pytest tests/ -v --alluredir=

# Use different HTML report path
pytest tests/ -v --html=reports/custom_report.html

# Override all defaults
pytest tests/ --override-ini="addopts=" -v
```

### Create Custom Configuration

```bash
# Use custom pytest config file
pytest tests/ -c custom_pytest.ini -v

# Show current configuration
pytest tests/ --co --setup-show

# Profile configuration overhead
pytest tests/ --collect-only --setup-show -v

# Verify configuration is loaded
pytest tests/ --fixtures | head -20
```

---

## 14. Docker Execution

### Build Docker Image

```bash
# Create Dockerfile (if not exists)
cat > Dockerfile << 'EOF'
FROM python:3.13-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN python -m playwright install chromium
COPY . .
CMD ["pytest", "tests/", "-v", "--html=reports/report.html"]
EOF

# Build image
docker build -t saucedemo-tests:latest .

# Build with custom name
docker build -t my-tests:1.0 .
```

### Run Tests in Docker

```bash
# Run all tests
docker run --rm saucedemo-tests:latest

# Run with volume mount (save reports locally)
docker run --rm -v $(pwd)/reports:/app/reports saucedemo-tests:latest

# Run smoke tests only
docker run --rm saucedemo-tests:latest pytest tests/ -m smoke -v

# Run specific test file
docker run --rm saucedemo-tests:latest pytest tests/test_login.py -v

# Run with custom command
docker run --rm saucedemo-tests:latest pytest tests/ -m regression -n 4 -v
```

### Docker with Reporting

```bash
# Run and save reports to host
docker run --rm \
  -v $(pwd)/reports:/app/reports \
  saucedemo-tests:latest \
  pytest tests/ -v \
    --html=reports/report.html \
    --alluredir=reports/allure \
    --junit-xml=reports/junit.xml

# Run with environment variables (for CI/CD)
docker run --rm \
  -e CI=true \
  -e BUILD_ID=123 \
  -v $(pwd)/reports:/app/reports \
  saucedemo-tests:latest

# Stop on failure (useful in CI)
docker run --rm saucedemo-tests:latest pytest tests/ -x -v
```

### Docker Compose (for complex setup)

```yaml
# docker-compose.yml
version: '3.8'
services:
  tests:
    build: .
    volumes:
      - ./reports:/app/reports
      - ./tests:/app/tests
    environment:
      - CI=true
      - PYTEST_ARGS=-v -m smoke
    command: pytest ${PYTEST_ARGS}
```

```bash
# Run with docker-compose
docker-compose up

# Run with specific service
docker-compose run tests pytest tests/ -m smoke -v

# Build and run
docker-compose up --build
```

---

## 15. Important Notes & Tips

### Common Gotchas

```bash
# ❌ WRONG: Forgetting to activate virtual environment
pytest tests/

# ✅ RIGHT: Activate venv first (Windows)
.venv\Scripts\Activate.ps1
pytest tests/

# ✅ RIGHT: Activate venv first (macOS/Linux)
source .venv/bin/activate
pytest tests/
```

### Installation & Verification

```bash
# Verify pytest is installed
pytest --version

# Check installed plugins
pytest --version

# List all available plugins
pip list | grep pytest

# Verify Playwright installation
python -m playwright install chromium --with-deps

# Check if chromium is available
python -c "from playwright.sync_api import sync_playwright; p = sync_playwright().start(); print('✅ Playwright OK')"
```

### Troubleshooting Commands

```bash
# Test fixture availability
pytest tests/ --fixtures

# Show fixture definitions
pytest tests/ --fixtures | grep -A 3 "page"

# Check for import errors
pytest tests/ --collect-only 2>&1 | head -20

# Debug marker registration
pytest tests/ --markers

# Verify test discovery
pytest tests/ --collect-only -q

# Check for syntax errors
python -m py_compile tests/test_*.py
```

### Performance Tips

```bash
# 🚀 Fastest: Smoke tests only
pytest tests/ -m smoke -v                          # ~20 seconds

# 🚀 Fast: Parallel full suite (4 workers)
pytest tests/ -n 4 -v                              # ~32 seconds

# 🔄 Medium: Sequential full suite
pytest tests/ -v                                   # ~128 seconds

# ⏸️ Slow: Full suite with debugging
pytest tests/ -v -s --pdb                          # Manual intervention
```

### Report View Commands

```bash
# View HTML report
open reports/report.html                           # macOS
start reports/report.html                          # Windows
xdg-open reports/report.html                       # Linux

# View Allure report (interactive)
allure serve reports/allure/

# Quick report verification
ls -lah reports/report.html                        # Check file size
file reports/report.html                           # Verify it's HTML
```

### CI/CD Integration Snippets

```yaml
# GitHub Actions Example
- name: Run Tests
  run: |
    pytest tests/ -v \
      --html=reports/report.html \
      --self-contained-html \
      --junit-xml=reports/junit.xml

- name: Upload Reports
  uses: actions/upload-artifact@v2
  if: always()
  with:
    name: test-reports
    path: reports/
```

```yaml
# GitLab CI Example
test:
  script:
    - pytest tests/ -v
      --html=reports/report.html
      --self-contained-html
      --junit-xml=reports/junit.xml
  artifacts:
    paths:
      - reports/
    reports:
      junit: reports/junit.xml
  allow_failure: false
```

### Copy-Paste Ready Commands by Scenario

```bash
# Scenario 1: I just want to know if tests pass
pytest tests/ -m smoke -v --tb=short

# Scenario 2: I broke something, fix it fast
pytest tests/ --lf -x -v -s

# Scenario 3: I want a full report
pytest tests/ -v --html=reports/report.html --self-contained-html \
  --alluredir=reports/allure --junit-xml=reports/junit.xml

# Scenario 4: I'm running CI/CD
pytest tests/ -v --junit-xml=reports/junit.xml --tb=short

# Scenario 5: I want to see what's slow
pytest tests/ -v --durations=20

# Scenario 6: I only care about cart and checkout
pytest tests/ -m "cart or checkout" -v

# Scenario 7: I want to run in parallel
pytest tests/ -n 4 -v

# Scenario 8: I need to debug a failing test
pytest tests/test_login.py::test_logout -v -s --pdb
```

### Quick Reference One-Liners

```bash
# All in one: reports + parallel + performance
pytest tests/ -n 4 -v --html=reports/report.html --self-contained-html \
  --alluredir=reports/allure --durations=10

# Smoke gate (pre-commit)
pytest tests/ -m smoke -x -v --tb=short

# Full regression (nightly)
pytest tests/ -v --junit-xml=reports/junit.xml --html=reports/report.html

# Debug single test
pytest tests/test_login.py::test_valid_login_standard_user -v -s -l

# Fastest turnaround (parallel smoke)
pytest tests/ -m smoke -n 4 -v

# Production deployment gate
pytest tests/ -m smoke -v --tb=line --junit-xml=reports/junit.xml

# Show coverage
pytest tests/ --cov=pages --cov-report=html

# Run and generate trends report
pytest tests/ -v > reports/run_$(date +%Y%m%d_%H%M%S).log
```

### Environment Setup

```bash
# Install all test dependencies
pip install -r requirements.txt

# Install Playwright browsers
python -m playwright install chromium

# Install with headless disabled (for debugging)
PLAYWRIGHT_HEADLESS=false pytest tests/test_login.py::test_valid_login -v -s

# Run with custom timeout
pytest tests/ --timeout=300 -v

# Run with verbose logging
PYTHONVERBOSE=2 pytest tests/ -v

# Run from project root (important)
cd saucedemo_automation/
pytest tests/ -v
```

### Windows PowerShell Specific

```powershell
# Activate virtual environment
.venv\Scripts\Activate.ps1

# Set execution policy if needed
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# Run tests with output to file
pytest tests/ -v | Tee-Object -FilePath reports/output.txt

# Open HTML report
Invoke-Item reports/report.html

# Run with environment variable
$env:CI='true'; pytest tests/ -v; $env:CI=''

# Measure execution time
Measure-Command { pytest tests/ -v } | Select-Object TotalSeconds
```

### macOS/Linux Specific

```bash
# Activate virtual environment
source .venv/bin/activate

# Run with output to file and screen
pytest tests/ -v 2>&1 | tee reports/output.txt

# Open HTML report
open reports/report.html

# Run with environment variable
CI=true pytest tests/ -v

# Measure execution time
time pytest tests/ -v

# Find and run specific tests by pattern
find tests/ -name "*.py" -path "*login*" | xargs pytest -v
```

---

## Quick Command Reference Card

```
╔════════════════════════════════════════════════════════════════════╗
║              PYTEST COMMAND QUICK REFERENCE CARD                  ║
╠════════════════════════════════════════════════════════════════════╣
║                                                                    ║
║ ALL TESTS:                                                         ║
║   pytest tests/                          (run all)                ║
║   pytest tests/ -v                       (verbose)                ║
║   pytest tests/ -v --durations=10        (show slowest)           ║
║                                                                    ║
║ BY MARKER:                                                         ║
║   pytest tests/ -m smoke                 (6 critical tests)       ║
║   pytest tests/ -m regression            (24 edge cases)          ║
║   pytest tests/ -m "smoke and login"     (combined)               ║
║                                                                    ║
║ BY FILE:                                                           ║
║   pytest tests/test_login.py             (8 tests)                ║
║   pytest tests/test_cart.py              (8 tests)                ║
║                                                                    ║
║ REPORTS:                                                           ║
║   pytest --html=reports/report.html      (HTML)                   ║
║   pytest --alluredir=reports/allure      (Allure)                 ║
║   allure serve reports/allure/           (View Allure)            ║
║                                                                    ║
║ DEBUG:                                                             ║
║   pytest tests/ -x                       (stop on first fail)     ║
║   pytest tests/ -v -s                    (show prints)            ║
║   pytest tests/ --lf                     (last failed)            ║
║   pytest tests/ --pdb                    (debugger on fail)       ║
║                                                                    ║
║ PARALLEL:                                                          ║
║   pytest tests/ -n 4                     (4 workers)              ║
║   pytest tests/ -n auto                  (all CPUs)               ║
║                                                                    ║
╚════════════════════════════════════════════════════════════════════╝
```

---

**Version:** 1.0  
**Last Updated:** March 23, 2026  
**Framework:** Pytest + Playwright  
**Tests:** 30 total (6 smoke, 24 regression)  
**Status:** ✅ Production Ready  

For more information, see:
- `pytest.ini` - Current configuration
- `TEST_EXECUTION_FLOW.md` - Detailed execution information
- `conftest.py` - Fixture definitions
