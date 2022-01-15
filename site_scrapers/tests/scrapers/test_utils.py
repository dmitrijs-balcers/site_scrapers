import unittest

from site_scrapers.scrapers.utils import parse_price


class UtilsTestCase(unittest.TestCase):
    def test_parse_price(self) -> None:
        self.assertEqual(parse_price("€42000"), 42000)  # add assertion here
        self.assertEqual(parse_price("30 900 € (0% PVN)"), 30900)  # add assertion here
        self.assertEqual(parse_price("26 900 €"), 26900)  # add assertion here
        self.assertEqual(parse_price("57 000 € (21% PVN)"), 57000)  # add assertion here


if __name__ == '__main__':
    unittest.main()
