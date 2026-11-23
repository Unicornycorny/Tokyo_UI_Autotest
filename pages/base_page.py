from typing import Pattern

import allure
from playwright.sync_api import Page, expect

from tools.logger import get_logger

logger = get_logger("BASE_PAGE")


class BasePage:
    def __init__(self, page: Page):
        self.page = page

        self.cart_button = page.get_by_test_id("header--button-5")

    def visit(self, url: str):
        step = f'Opening the url "{url}"'
        with allure.step(step):
            logger.info(step)
            self.page.goto(url, wait_until='domcontentloaded') # через networkidle падаем

    def check_current_url(self, expected_url: Pattern[str]):
        step = f'Checking that current url matches pattern "{expected_url.pattern}"'
        with allure.step(step):
            logger.info(step)
            expect(self.page).to_have_url(expected_url)

    def click_cart_button(self):
        step = 'Clicking the cart button in the header'
        with allure.step(step):
            logger.info(step)
            self.cart_button.click()
