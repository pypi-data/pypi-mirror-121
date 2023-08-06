import parsel

from extreme_parser.amazon.shop.model import Shop


def parse(html: str, s: Shop):
    sel = parsel.Selector(text=html)
    parse_seller(s, selector=sel)
    parse_name(s, selector=sel)
    parse_address(s, selector=sel)


def parse_seller(s: Shop, selector: parsel.Selector = None):
    s.seller = selector.xpath("//*[@id='sellerName']/text()").get()


def parse_name(s: Shop, selector: parsel.Selector = None):
    s.name = selector.xpath("//span[contains(text(), 'Business Name')]/following-sibling::text()").get()


def parse_address(s: Shop, selector: parsel.Selector = None):
    address = selector.xpath("string(//span[contains(text(), 'Business Address')]/following-sibling::ul)").get()
    if address == "":
        s.address = None
    else:
        s.address = address
