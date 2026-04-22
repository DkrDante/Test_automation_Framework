"""
UI-level fixtures for SatoriXR Playwright tests.

The `authenticated_page` fixture handles the two-step login flow
(email → verification code) and lands on the /home dashboard.

Usage
-----
Set the environment variables before running:

    export SATORIXR_EMAIL="your@email.com"
    export SATORIXR_OTP="123456"        # one-time code from inbox

Or pass them in via a CI secret / .env file loaded before pytest.
"""

import os
import pytest
from playwright.sync_api import sync_playwright


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _login(page, base_url: str, email: str, otp: str) -> None:
    """Perform the two-step SatoriXR login and wait for the dashboard."""
    page.goto(base_url)
    page.wait_for_load_state("networkidle")

    # Step 1 – enter email and request verification code
    page.fill("input#email", email)
    page.click("button:has-text('Send Verification Code')")

    # Step 2 – enter OTP (field appears after code is sent)
    page.wait_for_selector("input[type='text'][placeholder*='code']", timeout=15_000)
    page.fill("input[type='text'][placeholder*='code']", otp)
    page.click("button:has-text('Verify')")

    # Wait until redirected away from the login page
    page.wait_for_url("**/home**", timeout=20_000)
    page.wait_for_load_state("networkidle")


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture(scope="module")
def authenticated_page(config):
    """
    Module-scoped Playwright page that is already logged in.

    Reads credentials from environment variables:
      SATORIXR_EMAIL  – registered work email
      SATORIXR_OTP    – verification code (must be fetched before the run)
    """
    email = os.environ.get("SATORIXR_EMAIL", "")
    otp = os.environ.get("SATORIXR_OTP", "")

    if not email or not otp:
        pytest.skip(
            "Skipping authenticated UI tests: "
            "SATORIXR_EMAIL and SATORIXR_OTP env vars must be set."
        )

    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=config["headless"])
        context = browser.new_context()
        page = context.new_page()

        _login(page, config["base_url"], email, otp)

        yield page

        context.close()
        browser.close()
