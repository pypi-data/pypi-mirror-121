import parsel

from extreme_parser.etsy.product.model import Product


def parse(html: str, p: Product):
    sel = parsel.Selector(text=html)
    parse_title(p, selector=sel)


def parse_title(p: Product, selector: parsel.Selector = None):
    title = selector.xpath("//div[@id='listing-page-cart']//h1/text()").get()
    if title is None:
        p.title = None
    else:
        p.title = title.strip()
