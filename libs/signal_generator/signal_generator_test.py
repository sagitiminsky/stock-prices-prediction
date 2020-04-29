import unittest
from libs.signal_generator.signal_generator import SignalGenerator
import matplotlib.pyplot as plt
import libs.signal_generator.config


class StockRnnUnitTests(unittest.TestCase):
    def setUp(self):
        pass

    def test_create_signal_generator(self):
        self.assertTrue(SignalGenerator())

    def test_measure_signals(self):
        sg=SignalGenerator()
        for i in range(35):
            sg.measure()
            print(sg.stocks['sin']['x']._queue)

    def test_plot_graph(self):
        sg = SignalGenerator()
        for i in range(libs.signal_generator.config.window_size+25):
            sg.measure()


        #show signals
        plt.plot(list(sg.stocks['sin']['x']._queue),list(sg.stocks['sin']['y']._queue),'ro')
        plt.xlabel('x')
        plt.ylabel('sin(x)')
        plt.show()


if __name__ == '__main__':
    unittest.main()


