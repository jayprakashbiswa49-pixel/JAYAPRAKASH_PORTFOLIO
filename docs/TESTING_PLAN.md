# Testing Plan & Quality Assurance Strategy

**Testing Framework:** `pytest` + `pytest-flask`  
**Test Runner Target:** Python 3.10+ / Automated CI/CD Pipeline  

---

## 1. Testing Philosophy

The testing strategy guarantees that every route, template render, form validation rule, error boundary, and service fallback is rigorously verified via automated unit and integration tests.

### Quality Criteria:
- **Zero Flaky Tests**: Deterministic fixtures using isolated application contexts.
- **Fast Execution**: Entire test suite executes in < 3 seconds.
- **Defensive Coverage**: Coverage across all HTTP verbs, valid payloads, invalid edge cases, bot attacks, and missing assets.

---

## 2. Test Architecture & Fixtures (`tests/conftest.py`)

```python
import pytest
from app import create_app
from config import TestingConfig

@pytest.fixture
def app():
    """Create and configure a clean application instance for testing."""
    app = create_app(TestingConfig)
    yield app

@pytest.fixture
def client(app):
    """A test client for sending simulated HTTP requests."""
    return app.test_client()

@pytest.fixture
def runner(app):
    """A test CLI runner for invoking Flask commands."""
    return app.test_cli_runner()
```

---

## 3. Test Suites & Test Cases

### Suite 1: Route & View Tests (`tests/test_routes.py`)

| Test ID | Test Case | Target Endpoint | Input Condition | Expected Result |
| :--- | :--- | :--- | :--- | :--- |
| `TC-ROUTE-01` | Index Route Availability | `GET /` | Clean request | Status `200 OK`, HTML content type |
| `TC-ROUTE-02` | Personal Branding Present | `GET /` | Clean request | Body contains "Jayaprakash Biswal", "Bhubaneswar", "NIIS Group of Institutions" |
| `TC-ROUTE-03` | Flagship Projects Present | `GET /` | Clean request | Body contains "Glint", "Customer Churn Prediction", and valid repo links |
| `TC-ROUTE-04` | Skills & Certifications Present | `GET /` | Clean request | Body contains "Python", "Flask", "Pandas", "Scikit-learn", "CodeWithHarry" |
| `TC-ROUTE-05` | Resume Endpoint Inline | `GET /resume` | No query params | Status `200 OK`, `Content-Type: application/pdf`, `Content-Disposition: inline` |
| `TC-ROUTE-06` | Resume Endpoint Download | `GET /resume?download=1` | `download=1` | Status `200 OK`, `Content-Disposition: attachment` |
| `TC-ROUTE-07` | Health Check Route | `GET /health` | Clean request | Status `200 OK`, JSON `{"status": "ok", "app": "Jayaprakash Biswal Portfolio"}` |
| `TC-ROUTE-08` | 404 Error Handler | `GET /non-existent-route` | Invalid URL | Status `404 Not Found`, renders custom Neumorphic 404 template |

---

### Suite 2: Form Validation & Security Tests (`tests/test_forms.py`)

| Test ID | Test Case | Target Endpoint | Input Condition | Expected Result |
| :--- | :--- | :--- | :--- | :--- |
| `TC-FORM-01` | Valid Form Submission (AJAX) | `POST /contact` | Valid JSON payload with name, email, subject, message | Status `200 OK`, JSON `{"success": true}` |
| `TC-FORM-02` | Valid Form Submission (POST Form) | `POST /contact` | Valid form-encoded data | Status `302 Found` (redirect to `/#contact`), flashed success |
| `TC-FORM-03` | Missing Required Fields | `POST /contact` | Empty message / missing email | Status `400 Bad Request`, validation errors returned |
| `TC-FORM-04` | Malformed Email Syntax | `POST /contact` | Email = `"not-an-email"` | Status `400 Bad Request`, email validation error returned |
| `TC-FORM-05` | Honeypot Bot Interception | `POST /contact` | `hp_website = "http://spam.com"` | Status `200 OK` (silent discard), submission NOT logged/sent |
| `TC-FORM-06` | Message Length Overflow | `POST /contact` | Message > 3000 chars | Status `400 Bad Request`, length constraint triggered |
| `TC-FORM-07` | CSRF Enforcement | `POST /contact` | Missing CSRF token when `WTF_CSRF_ENABLED=True` | Status `400 Bad Request`, CSRF token missing error |

---

### Suite 3: Service & Resilience Tests (`tests/test_services.py`)

| Test ID | Test Case | Target | Condition | Expected Result |
| :--- | :--- | :--- | :--- | :--- |
| `TC-SRV-01` | Email Service Fallback | `EmailService.send_inquiry` | SMTP unconfigured | Returns `True` (logged safely), no uncaught exception |
| `TC-SRV-02` | Data Layer Integrity | `portfolio_data.py` | Load static data structures | Verifies project links, valid URLs, non-empty skill categories |

---

## 4. Test Execution Instructions

Run all test suites locally:
```bash
pytest -v
```

Run with coverage reporting:
```bash
pytest --cov=app --cov-report=term-missing
```
