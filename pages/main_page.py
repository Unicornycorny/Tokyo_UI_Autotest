import re

import allure
from playwright.sync_api import Page

from pages.base_page import BasePage
from tools.logger import get_logger

logger = get_logger("MAIN_PAGE")


class MainPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        
        # Мобильная копия лежит в обёртке с классом mobileMenu и data-testid="mobile-menu", её ссылки исключаем
        self.catalogue_menu_links = page.locator(
            '[data-testid^="verticalMenu--Link-"]:not(.mobileMenu[data-testid="mobile-menu"] *)'
        )

    def click_catalogue_category(self, category: str):
        step = f'Opening catalogue category "{category}"'
        with allure.step(step):
            logger.info(step)
            self.catalogue_menu_links.filter(has_text=re.compile(rf"^{re.escape(category)}$")).click()
        self.check_current_url(re.compile(r".*/catalogue/[^/]+$"))
