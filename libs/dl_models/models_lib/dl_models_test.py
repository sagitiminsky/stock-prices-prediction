import unittest
from libs.stock_object.get_stock_info import GetStockInfo
from unittest.mock import Mock


class StockRnnUnitTests(unittest.TestCase):
    def setUp(self):
        self.stock=['FB']
        self.window_size = 20

    def test_1(self):
        self.assertTrue(True)


if __name__ == '__main__':
    unittest.main()


