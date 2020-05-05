import unittest
from libs.stocks.graphs.graphs import Graphs
from unittest.mock import Mock
import libs.stocks.graphs.config


class GraphsTest(unittest.TestCase):
    def setUp(self):
        self.time_scales= libs.stocks.graphs.config.time_scales
        self.stock_name='FB'

    def test_create_Graphs(self):
        self.assertTrue(Graphs(stock_name=self.stock_name,mock=Mock()))



if __name__ == '__main__':
    unittest.main()


