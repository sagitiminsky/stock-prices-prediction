import unittest
from libs.stock_object.get_stock_info import GetStocksInfo
from unittest.mock import Mock
import apps.config


class StockRnnUnitTests(unittest.TestCase):
    def setUp(self):
        self.stock_names=apps.config.stock_names
        self.window_size = apps.config.window_size

    def test_create_GetStockInfo(self):
        """
        Test libs/get_stock_info.py

        Creates an GetStockInfo object, and test it creation of obejct is successful
        """
        self.assertTrue(GetStocksInfo(self.window_size, self.stock_names))


    def test_measure_stock(self):
        """
        Test libs/get_stock_info.py
        - preform test_create_GetStockInfo
        - Use mock to imitate reading from stock prices DB and test measure_stock
        """

        stockObj=GetStocksInfo(self.window_size, self.stock_names)
        self.assertTrue(stockObj.measure(mock=Mock()))


if __name__ == '__main__':
    unittest.main()


