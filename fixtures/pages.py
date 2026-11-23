import pytest
from playwright.sync_api import Page

from pages.cart_page import CartPage
from pages.catalogue_page import CataloguePage
from pages.main_page import MainPage


@pytest.fixture
def main_page(chrome_page: Page) -> MainPage:
    return MainPage(page=chrome_page)


@pytest.fixture
def catalogue_page(chrome_page: Page) -> CataloguePage:
    return CataloguePage(page=chrome_page)


@pytest.fixture
def cart_page(chrome_page: Page) -> CartPage:
    return CartPage(page=chrome_page)
