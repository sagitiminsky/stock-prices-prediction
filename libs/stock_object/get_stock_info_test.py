import unittest
from libs.stock_object.get_stock_info import GetStockInfo
from unittest.mock import Mock


class StockRnnUnitTests(unittest.TestCase):
    def setUp(self):
        self.stock=['FB']
        self.window_size = 20

    def test_create_GetStockInfo(self):
        """
        Test libs/get_stock_info.py

        Creates an GetStockInfo object, and test it creation of obejct is successful
        """
        self.assertTrue(GetStockInfo(self.window_size, self.stock))


    def test_measure_stock(self):
        """
        Test libs/get_stock_info.py
        - preform test_create_GetStockInfo
        - Use mock to imitate reading from stock prices DB and test measure_stock
        """

        stockObj=GetStockInfo(self.window_size, self.stock)
        self.assertTrue(stockObj.measure_stock(mock=Mock()))


if __name__ == '__main__':
    unittest.main()


