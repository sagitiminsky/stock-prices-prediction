from libs.stocks.queues.queue.queue import Queue
import apps.ai.config as config
import numpy as np
from itertools import cycle
from libs.stocks.stock_object.stock_obj import StockObj


time_scale2seconds = {
    '1s': 1,
    '1m': 60,
    '2m': 120,
    '5m': 300,
    '15m': 900,
    '30m': 1800,
    '1h': 3600,
    '1d': 86400,
    '5d': 432000,
    '1mo': 2592000,  # todo: depends which month
    '3mo': 7776000,
}

class SignalGenerator:
    def __init__(self,mock=None):
        self.time_scales = {'1s':cycle(np.arange(0, 2 * np.pi, config.max_window_size['1s'])),
                            '1m':cycle(np.arange(0, 2 * np.pi, config.max_window_size['1m'])),
                            '2m': cycle(np.arange(0, 2 * np.pi, config.max_window_size['2m'])),
                            '5m': cycle(np.arange(0, 2 * np.pi, config.max_window_size['5m'])),
                            '15m': cycle(np.arange(0, 2 * np.pi, config.max_window_size['15m'])),
                            '30m': cycle(np.arange(0, 2 * np.pi, config.max_window_size['30m'])),
                            '1h': cycle(np.arange(0, 2 * np.pi, config.max_window_size['1h'])),
                            '1d': cycle(np.arange(0, 2 * np.pi, config.max_window_size['1d'])),
                            '5d': cycle(np.arange(0, 2 * np.pi, config.max_window_size['5d'])),
                            '1mo': cycle(np.arange(0, 2 * np.pi, config.max_window_size['1mo'])),
                            '3mo': cycle(np.arange(0, 2 * np.pi, config.max_window_size['3mo'])),
                            }

        self.signals={}
        for signal_name in config.signals_names:
            self.signals[signal_name] = {
                'link':signal_name,'stock_obj': self.time_scales}


    def measure(self,mock=None):
        pass