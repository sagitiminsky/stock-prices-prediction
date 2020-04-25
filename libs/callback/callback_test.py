import unittest
from unittest.mock import Mock
from libs.callback.callback import CallBack

class StockRnnUnitTests(unittest.TestCase):
    def setUp(self):
        pass
    def test_setup(self):
        self.assertTrue(CallBack())
if __name__ == '__main__':
    unittest.main()


