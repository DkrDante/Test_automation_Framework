import pytest
from playwright.sync_api import sync_playwright
import yaml

def load_config():
    with open("config/config.yaml") as f:
        return yaml.safe_load(f)

@pytest.fixture(scope="session")
def config():
    return load_config()

@pytest.fixture
def page(config):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=config["headless"])
        page = browser.new_page()
        yield page
        browser.close()