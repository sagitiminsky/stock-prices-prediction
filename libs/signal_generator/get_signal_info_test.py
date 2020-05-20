import unittest
from libs.signal_generator.get_signal_info import GetSignalInfo

class StockRnnUnitTests(unittest.TestCase):
    def setUp(self):
        pass

    def test_get_signal_info(self):
        self.assertTrue(GetSignalInfo())
    def test_measure(self):
        g=GetSignalInfo()
        g.measure()


if __name__ == '__main__':
    unittest.main()


