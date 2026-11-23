from typing import Generator

import pytest
from _pytest.fixtures import SubRequest
from playwright.sync_api import Playwright, Page

from config import settings
from tools.playwright.pages import initialize_playwright_page


@pytest.fixture
def chrome_page(request: SubRequest, playwright: Playwright) -> Page:
    yield from initialize_playwright_page(
        playwright,
        test_name=request.node.name
    )