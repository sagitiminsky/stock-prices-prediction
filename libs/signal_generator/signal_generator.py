from libs.stocks.queues.queue.queue import Queue
import apps.ai.config as config
import numpy as np
from itertools import cycle


class SignalGenerator:
    def __init__(self):
        self.delta = config.delta
        self.time_stamps = cycle(np.arange(0, 2 * np.pi, self.delta))
        self.stocks = {}
        self.signals_names = config.signals_names

        for signal_name in self.signals_names:
            self.stocks[signal_name] = {
                'x': Queue(init_list=[0] * config.max_window_size['1s'], maxlen=config.max_window_size['1s']),
                           'y':Queue(init_list=[0] * config.max_window_size['1s'], maxlen=config.max_window_size['1s'])
            }

    def measure(self):
        time_stamp = self.time_stamps.__next__()
        for signal_name in self.signals_names:
            self.stocks[signal_name]['x'].enqueue(time_stamp) if signal_name == 'sin' else self.stocks[signal_name][
                'x'].enqueue(time_stamp)
            self.stocks[signal_name]['y'].enqueue(np.sin(time_stamp)) if signal_name == 'sin' else \
            self.stocks[signal_name]['y'].enqueue(np.cos(time_stamp))
