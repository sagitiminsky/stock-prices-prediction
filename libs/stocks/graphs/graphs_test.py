import unittest
from libs.stocks.graphs.graphs import Graphs_Obj
from unittest.mock import Mock
import apps.ai.config as config


class GraphsTest(unittest.TestCase):
    def setUp(self):
        self.time_scales = config.time_scales
        self.stock_name='FB'

    def test_create_Graphs(self):
        self.assertTrue(Graphs_Obj(stock_name=self.stock_name,mock=Mock()))



if __name__ == '__main__':
    unittest.main()


