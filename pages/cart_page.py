import re

import allure
from playwright.sync_api import Page, Locator, expect

from pages.base_page import BasePage
from tools.logger import get_logger
from tools.prices import price_pattern

logger = get_logger("CART_PAGE")


class CartPage(BasePage):

    def __init__(self, page: Page):
        super().__init__(page)

        self.cart_modal = page.locator(".basketModal")
        self.close_button = self.cart_modal.get_by_test_id("basketModal--button-0")
        self.title = self.cart_modal.locator(".basketItem__title")
        self.total_price = self.cart_modal.locator(".fixedField__sum .textH2")

        #строка корзины - родитель её кнопки удалить
        self.cart_items = self.cart_modal.get_by_test_id(re.compile(r"^subItemBasket--button-\d+$")).locator("xpath=..")

    def get_cart_item(self, name: str) -> Locator:
        return self.cart_items.filter(
            has=self.page.locator(".name", has_text=re.compile(rf"^{re.escape(name)}$"))
        )

    def check_visible(self):
        step = 'Checking that the cart is open'
        with allure.step(step):
            logger.info(step)
            expect(self.close_button).to_be_visible()
            expect(self.title).to_have_text("Корзина")

    def check_items_count(self, count: int):
        step = f'Checking that the cart contains {count} item(s)'
        with allure.step(step):
            logger.info(step)
            expect(self.cart_items).to_have_count(count)

    def check_product(self, name: str, quantity: int, total_price: int):
        step = f'Checking that the cart contains product "{name}": {quantity} pcs for {total_price} ₽'
        with allure.step(step):
            logger.info(step)
            cart_item = self.get_cart_item(name)
            expect(cart_item).to_be_visible()
            expect(cart_item.locator(".stepperValue")).to_have_text(str(quantity))
            expect(cart_item.locator(".subItemBasket__options__price")).to_have_text(price_pattern(total_price))

    def check_total_price(self, total_price: int):
        step = f'Checking that the cart total is {total_price} ₽'
        with allure.step(step):
            logger.info(step)
            expect(self.total_price).to_have_text(price_pattern(total_price))
