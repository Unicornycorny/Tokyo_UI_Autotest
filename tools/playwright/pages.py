from typing import Generator

import allure
from playwright.sync_api import Playwright, Browser, Page

from config import settings


def initialize_playwright_browser(playwright: Playwright) -> Browser:
    browser = playwright.chromium.launch(
        channel=settings.browser,
        headless=settings.headless,
    )

    yield browser

    browser.close()


def initialize_playwright_page(browser: Browser, test_name: str) -> Page:
    context = browser.new_context(
        base_url=settings.get_base_url(),
        viewport={"width": 1920, "height": 1080},
        locale="ru-RU",
        record_video_dir=settings.videos_dir,
    )
    context.tracing.start(screenshots=True, snapshots=True, sources=True)
    page = context.new_page()

    yield page

    tracing_file = settings.tracing_dir.joinpath(f"{test_name}.zip")
    context.tracing.stop(path=tracing_file)
    context.close()

    allure.attach.file(tracing_file, name="trace", extension="zip")
    allure.attach.file(page.video.path(), name="video", attachment_type=allure.attachment_type.WEBM)
