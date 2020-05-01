import unittest
from libs.stock_object.graphs.graphs import Graphs
import libs.stock_object.graphs.config
from unittest.mock import Mock



class StockRnnUnitTests(unittest.TestCase):
    def setUp(self):
        self.time_scales=libs.stock_object.graphs.config.time_scales
        self.stock_name='FB'

    def test_create_Graphs(self):
        self.assertTrue(Graphs(stock_name=self.stock_name,mock=Mock()))



if __name__ == '__main__':
    unittest.main()


