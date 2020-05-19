import apps.ai.config as config
from libs.stocks.stock_object.stock_obj import StockObj
import threading
import numpy as np
from itertools import cycle


class GetSignalInfo:
    def __init__(self, mock=None):
        self.signal_names = config.signal_names
        self.signals = {}
        for signal_name in self.signal_names:
            self.signals[signal_name] = {'cycle': cycle(np.linspace(0, 2 * np.pi, config.max_window_size['1s'])),
                                         'stock_obj': StockObj(stock_name=signal_name, mock=mock, sin=True)}

    def measure(self):
        threading.Timer(1.0, self.measure).start()
        for signal_name in self.signal_names:
            value, volume = self.signals[signal_name]['cycle'].__next__(), 0

            stock_object = self.signals[signal_name]['stock_obj']
            stock_object.enqueue({'value': value, 'volume': volume})
