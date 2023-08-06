import json
from typing import Union

import parsel

from extreme_parser.etsy.product.model import Product
from extreme_parser.util.parse import parse_number


def parse_context(selector: parsel.Selector = None) -> Union[dict, None]:
    c = selector.re_first(r'Etsy.Context=({.*})')
    if c is None:
        return None
    else:
        return json.loads(c)


def parse(html: str, p: Product):
    sel = parsel.Selector(text=html)
    parse_title(p, selector=sel)
    parse_shop_id(p, selector=sel)
    parse_price(p, selector=sel)
    parse_favorites(p, selector=sel)
    parse_stock(p, selector=sel)
    parse_reviews(p, selector=sel)
    parse_currency(p, selector=sel)


def parse_title(p: Product, selector: parsel.Selector = None):
    title = selector.xpath("//div[@id='listing-page-cart']//h1/text()").get()
    if title is None:
        p.title = None
    else:
        p.title = title.strip()


def parse_shop_id(p: Product, selector: parsel.Selector = None):
    context = parse_context(selector)
    if context is None:
        p.shop_id = None
        return

    try:
        shop_id = context.get("data").get("shop_id")
    except AttributeError:
        p.shop_id = None
    else:
        p.shop_id = shop_id


def parse_price(p: Product, selector: parsel.Selector = None):
    context = parse_context(selector)
    if context is None:
        p.price = None
        return

    try:
        price = context.get("data").get("granify").get("product").get("price")
    except AttributeError:
        p.price = None
    else:
        p.price = price


def parse_favorites(p: Product, selector: parsel.Selector = None):
    favorites = selector.xpath(
        "normalize-space((//a[contains(text(), 'favorite')]|//a[contains(text(), 'favourite')])/text())"
    ).get()
    if favorites == "":
        p.favorites = None
        return

    if "One" in favorites:
        p.favorites = 1
        return

    favorites = parse_number(favorites)
    if favorites is None:
        p.favorites = None
    else:
        p.favorites = favorites


def parse_stock(p: Product, selector: parsel.Selector = None):
    context = parse_context(selector)
    if context is None:
        p.stock = None
        return

    try:
        stock = context.get("data").get("granify").get("product").get("in_stock")
    except AttributeError:
        p.stock = None
    else:
        p.stock = stock


def parse_reviews(p: Product, selector: parsel.Selector = None):
    reviews = selector.xpath("normalize-space(//button[@id='same-listing-reviews-tab']/span/text())").get()
    if reviews == "":
        p.reviews = None
        return

    reviews = reviews.replace(",", "")
    if reviews.isdigit():
        p.reviews = int(reviews)
    else:
        p.reviews = None


def parse_currency(p: Product, selector: parsel.Selector = None):
    context = parse_context(selector)
    if context is None:
        p.currency = None
        return

    try:
        currency = context.get("data").get("locale_settings").get("currency").get("code")
    except AttributeError:
        p.currency = None
    else:
        p.currency = currency
