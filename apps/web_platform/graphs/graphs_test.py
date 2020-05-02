import unittest
from apps.web_platform.graphs.graphs import Graphs
import apps.web_platform.graphs.config
from unittest.mock import Mock



class StockRnnUnitTests(unittest.TestCase):
    def setUp(self):
        self.time_scales= apps.web_platform.graphs.config.time_scales
        self.stock_name='FB'

    def test_create_Graphs(self):
        self.assertTrue(Graphs(stock_name=self.stock_name,mock=Mock()))



if __name__ == '__main__':
    unittest.main()


