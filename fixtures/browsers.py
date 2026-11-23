from typing import Generator

import pytest
from _pytest.fixtures import SubRequest
from playwright.sync_api import Playwright, Browser, Page

from config import settings
from tools.playwright.pages import initialize_playwright_browser, initialize_playwright_page

#браузер
@pytest.fixture(scope="session")
def chrome_browser(playwright: Playwright) -> Browser:
    yield from initialize_playwright_browser(playwright)


#клиент
@pytest.fixture
def chrome_page(request: SubRequest, chrome_browser: Browser) -> Page:
    yield from initialize_playwright_page(
        chrome_browser,
        test_name=request.node.name
    )