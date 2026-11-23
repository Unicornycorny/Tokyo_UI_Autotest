import re


def parse_price(text: str) -> int:
    """'1 770 ₽...' -> 1770"""
    current_price = text.split("₽")[0]
    return int(re.sub(r"\D", "", current_price))


def price_pattern(price: int) -> re.Pattern[str]:
    """1770 -> шаблон для текста цены"""
    thousands = f"{price:,}".split(",")
    return re.compile("^" + r"\s?".join(thousands) + r"\s?₽")
