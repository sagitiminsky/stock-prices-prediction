import unittest
from libs.get_stock_info import GetStockInfo
from unittest.mock import Mock


class DocumentClassificationTest(unittest.TestCase):
    def setUp(self):
        self.stock=['FB']
        self.window_size = 20

    def test_1(self):
        """
        Test libs/get_stock_info.py

        Creates an GetStockInfo object, and test it creation of obejct is successful
        """
        self.assertTrue(GetStockInfo(self.window_size, self.stock))


    def test_2(self):
        """
        Test libs/get_stock_info.py

        Creates an GetStockInfo object, use mock in oreder to mock reading from stock prices DB
        """

        stockObj=GetStockInfo(self.window_size, self.stock)
        self.assertTrue(stockObj.measure_stock(mock=Mock()))

if __name__ == '__main__':
    unittest.main()


