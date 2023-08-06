from unittest import TestCase

from extreme_parser.amazon.search.parse import parse_products, parse_max_page, parse_results, parse_brands
from extreme_parser.util import read_file


class ParseTest(TestCase):
    def test_parse_products(self):
        html = read_file("./testdata/1.html")
        products = parse_products(html)
        self.assertEqual(69, len(products))

    def test_parse_max_page(self):
        html = read_file("./testdata/1.html")
        max_page = parse_max_page(html)
        self.assertEqual(7, max_page)

    def test_parse_results(self):
        html = read_file("./testdata/1.html")
        results = parse_results(html)
        self.assertEqual(40000, results)
        html = read_file("./testdata/2.html")
        results = parse_results(html)
        self.assertEqual(8, results)

    def test_parse_brands(self):
        html = read_file("./testdata/2.html")
        brands = parse_brands(html)
        self.assertEqual(['TEONE', 'Wieco'], brands)
