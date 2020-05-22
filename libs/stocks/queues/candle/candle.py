from libs.stocks.queues.queue.queue import Queue
import apps.ai.config as config
import numpy as np


class Candle():
    '''
    Thread-safe, memory-efficient, maximally-sized queue supporting queueing and
    dequeueing in worst-case O(1) time.
    '''

    def __init__(self, init_dict, time_scale):
        '''
        Initialize this queue to the empty queue.

        Parameters
        ----------
        max_size : int
            Maximum number of items contained in this queue. Defaults to 10.
        '''
        self.candle = {'open': Queue(init_list=init_dict['open'], maxlen=config.max_window_size[time_scale]),
                       'low': Queue(init_list=init_dict['low'], maxlen=config.max_window_size[time_scale]),
                       'high': Queue(init_list=init_dict['high'], maxlen=config.max_window_size[time_scale]),
                       'close': Queue(init_list=init_dict['close'], maxlen=config.max_window_size[time_scale]),
                       'volume': Queue(init_list=init_dict['volume'], maxlen=config.max_window_size[time_scale])
                       }

    def enqueue(self, item):
        '''
        Queues the passed item (i.e., pushes this item onto the tail of this
        queue).

        If this queue is already full, the item at the head of this queue
        is silently removed from this queue *before* the passed item is
        queued.
        '''

        self.candle['open'].enqueue(item['open'])
        self.candle['low'].enqueue(item['low'])
        self.candle['high'].enqueue(item['high'])
        self.candle['close'].enqueue(item['close'])
        self.candle['volume'].enqueue(item['volume'])

    def get_vstacked_queues(self):
        return np.vstack((
            np.array(list(self.candle['high']._norm_queue)),
            np.array(list(self.candle['close']._norm_queue)),
            np.array(list(self.candle['open']._norm_queue)),
            np.array(list(self.candle['low']._norm_queue)),
            np.array(list(self.candle['volume']._norm_queue))))
