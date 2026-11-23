import re

import allure
from playwright.sync_api import Page, Locator, expect

from pages.base_page import BasePage
from tools.logger import get_logger
from tools.prices import parse_price

logger = get_logger("CATALOGUE_PAGE")


class CataloguePage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)

        self.title = page.locator("h1")
        self.subcategory_buttons = page.get_by_test_id(re.compile(r"^catalogue--button-\d+$"))

        # Testid элементов внутри карточки товара
        self.product_link_test_id = re.compile(r"^dishes-item--Link-\d+$")
        self.add_to_cart_button_test_id = re.compile(r"^dishes-item--button-\d+$")
        self.increase_quantity_button_test_id = "stepper--button-1"  # stepper--button-0 — это «−»

        #карточка - родитель её ссылки
        self.product_cards = page.get_by_test_id(self.product_link_test_id).locator("xpath=..")

    def get_product_card(self, index: int) -> Locator:
        return self.product_cards.nth(index)

    def check_visible_title(self, title: str):
        step = f'Checking that catalogue page title is "{title}"'
        with allure.step(step):
            logger.info(step)
            expect(self.title).to_have_text(title)

    def click_subcategory(self, subcategory: str):
        step = f'Opening subcategory "{subcategory}"'
        with allure.step(step):
            logger.info(step)
            self.subcategory_buttons.filter(has_text=re.compile(rf"^{re.escape(subcategory)}$")).click()
        self.check_current_url(re.compile(r".*/catalogue/[^/]+/[^/]+$"))

    def get_product_name(self, index: int) -> str:
        step = f'Getting the name of product #{index + 1}'
        with allure.step(step):
            logger.info(step)
            name = self.get_product_card(index).get_by_test_id(self.product_link_test_id).inner_text()
            allure.attach(name, name="product name", attachment_type=allure.attachment_type.TEXT)
            return name

    def get_product_price(self, index: int) -> int:
        step = f'Getting the price of product #{index + 1}'
        with allure.step(step):
            logger.info(step)
            price = parse_price(self.get_product_card(index).locator(".dishesItem__price").inner_text())
            allure.attach(str(price), name="product price", attachment_type=allure.attachment_type.TEXT)
            return price

    def add_product_to_cart(self, index: int):
        step = f'Adding product #{index + 1} to the cart'
        with allure.step(step):
            logger.info(step)
            card = self.get_product_card(index)
            card.get_by_test_id(self.add_to_cart_button_test_id).click()
            expect(card.locator(".stepperValue")).to_have_text("1")

    def increase_product_quantity(self, index: int, quantity: int):
        step = f'Increasing quantity of product #{index + 1} to {quantity}'
        with allure.step(step):
            logger.info(step)
            card = self.get_product_card(index)
            quantity_value = card.locator(".stepperValue")
            increase_button = card.get_by_test_id(self.increase_quantity_button_test_id)

            #ждём, пока обновится счётчик
            for expected_quantity in range(int(quantity_value.inner_text()) + 1, quantity + 1):
                increase_button.click()
                expect(quantity_value).to_have_text(str(expected_quantity))
