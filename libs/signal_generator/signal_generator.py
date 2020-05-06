from libs.stocks.queue.queue import Queue
import libs.signal_generator.config
import numpy as np
from itertools import cycle


class SignalGenerator:
    def __init__(self):
        self.window_size=libs.signal_generator.config.window_size
        self.delta=libs.signal_generator.config.delta
        self.time_stamps=cycle(np.arange(0,2*np.pi,self.delta))
        self.stocks={}
        self.signals_names=libs.signal_generator.config.signals_names

        for signal_name in self.signals_names:
            self.stocks[signal_name] = {'x': Queue(max_size=self.window_size) , 'y':Queue(max_size=self.window_size)}

    def measure(self):
        time_stamp=self.time_stamps.__next__()
        for signal_name in self.signals_names:
            self.stocks[signal_name]['x'].enqueue(time_stamp) if signal_name == 'sin' else self.stocks[signal_name]['x'].enqueue(time_stamp)
            self.stocks[signal_name]['y'].enqueue(np.sin(time_stamp)) if signal_name=='sin' else self.stocks[signal_name]['y'].enqueue(np.cos(time_stamp))






