import allure
import pytest
from allure_commons.types import Severity

from config import settings
from pages.cart_page import CartPage
from pages.catalogue_page import CataloguePage
from pages.main_page import MainPage
from tools.allure.features import AllureFeature
from tools.allure.tags import AllureTag
from tools.routes import AppRoute

FIRST_PRODUCT_QUANTITY = 3


@pytest.mark.cart
@pytest.mark.regression
@allure.tag(AllureTag.REGRESSION, AllureTag.CART, AllureTag.CATALOGUE)
@allure.feature(AllureFeature.CART)
@allure.suite(AllureFeature.CART)
class TestCart:
    @allure.title("Add two different products to the cart, the first one in quantity 3")
    @allure.severity(Severity.CRITICAL)
    def test_add_two_products_to_cart(
            self,
            main_page: MainPage,
            catalogue_page: CataloguePage,
            cart_page: CartPage
    ):
        main_page.visit(AppRoute.MAIN)
        main_page.click_catalogue_category(settings.test_data.category)
        catalogue_page.check_visible_title(settings.test_data.category)
        catalogue_page.click_subcategory(settings.test_data.subcategory)
        catalogue_page.check_visible_title(settings.test_data.subcategory)

        first_product_name = catalogue_page.get_product_name(index=0)
        first_product_price = catalogue_page.get_product_price(index=0)
        catalogue_page.add_product_to_cart(index=0)
        catalogue_page.increase_product_quantity(index=0, quantity=FIRST_PRODUCT_QUANTITY)

        second_product_name = catalogue_page.get_product_name(index=1)
        second_product_price = catalogue_page.get_product_price(index=1)
        catalogue_page.add_product_to_cart(index=1)

        catalogue_page.click_cart_button()
        cart_page.check_visible()
        cart_page.check_items_count(2)
        cart_page.check_product(
            name=first_product_name,
            quantity=FIRST_PRODUCT_QUANTITY,
            total_price=first_product_price * FIRST_PRODUCT_QUANTITY
        )
        cart_page.check_product(
            name=second_product_name,
            quantity=1,
            total_price=second_product_price
        )
        cart_page.check_total_price(first_product_price * FIRST_PRODUCT_QUANTITY + second_product_price)
