from typing import Union

import parsel

from extreme_parser.util.parse import parse_number


def parse_products(html: str) -> list:
    sel = parsel.Selector(text=html)
    asin = sel.xpath("//@data-asin").getall()
    asin = list(filter(lambda s: s != '', asin))
    return asin


def parse_max_page(html: str) -> Union[int, None]:
    sel = parsel.Selector(text=html)
    max_page = sel.xpath("//ul[@class='a-pagination']/li[last()-1]/text()").get()
    if max_page and max_page.isdigit():
        return int(max_page)
    else:
        return None


def parse_results(html: str) -> Union[int, None]:
    sel = parsel.Selector(text=html)
    results = sel.xpath(
        'normalize-space(//span[@data-component-type="s-result-info-bar"]//span[contains(text(), "result")]/text())'
    ).get()
    if results == "":
        return None

    results = parse_number(results.replace(",", ""), first=False)
    if results is None or isinstance(results[-1], float):
        return None
    else:
        return results[-1]
