from libs.stocks.graphs.graphs import Graphs_Obj
from libs.stocks.queues.queue.queue import Queue
from libs.stocks.queues.queue_obj.queue_obj import QueueObejct
import apps.ai.config as config


class StockObj():
    '''
    Thread-safe, memory-efficient, maximally-sized queue supporting queueing and
    dequeueing in worst-case O(1) time.
    '''

    def __init__(self, stock_name, mock=None):
        '''
        Initialize this queue to the empty queue.

        Parameters
        ----------
        max_size : int
            Maximum number of items contained in this queue. Defaults to 10.
        '''

        self.sec_counter = 0

        # graphs - scraped
        self.graphs_obj = Graphs_Obj(stock_name=stock_name, mock=mock)
        self.time_scales = {
            '1s': Queue(init_list=[0] * config.max_window_size['1s'], maxlen=config.max_window_size['1s']),
            '1m': QueueObejct(init_dict=self.graphs_obj.graphs['1m'], time_scale='1m'),
            '2m': QueueObejct(init_dict=self.graphs_obj.graphs['2m'], time_scale='2m'),
            '5m': QueueObejct(init_dict=self.graphs_obj.graphs['5m'], time_scale='5m'),
            '15m': QueueObejct(init_dict=self.graphs_obj.graphs['15m'], time_scale='15m'),
            '30m': QueueObejct(init_dict=self.graphs_obj.graphs['30m'], time_scale='30m'),
            '90m': QueueObejct(init_dict=self.graphs_obj.graphs['90m'], time_scale='90m'),
            '1h': QueueObejct(init_dict=self.graphs_obj.graphs['1h'], time_scale='1h'),
            '1d': QueueObejct(init_dict=self.graphs_obj.graphs['1d'], time_scale='1d'),
            '5d': QueueObejct(init_dict=self.graphs_obj.graphs['5d'], time_scale='5d'),
            '1wk': QueueObejct(init_dict=self.graphs_obj.graphs['1wk'], time_scale='1wk'),
            '1mo': QueueObejct(init_dict=self.graphs_obj.graphs['1mo'], time_scale='1mo'),
            '3mo': QueueObejct(init_dict=self.graphs_obj.graphs['3mo'], time_scale='3mo')
        }
        pass

    def enqueue(self, item):
        '''
        Queues the passed item (i.e., pushes this item onto the tail of this
        queue).

        If this queue is already full, the item at the head of this queue
        is silently removed from this queue *before* the passed item is
        queued.
        '''
        self.time_scales['1s'].enqueue(item['value'])
        self.sec_counter = self.sec_counter + 1
        if self.sec_counter % config.time_scale2seconds['1m'] == 0: self.time_scales['1m'].enqueue(
            self.insert('1m', item['volume']))
        if self.sec_counter % config.time_scale2seconds['2m'] == 0: self.time_scales['2m'].enqueue(
            self.insert('2m', item['volume']))
        if self.sec_counter % config.time_scale2seconds['5m'] == 0: self.time_scales['5m'].enqueue(
            self.insert('5m', item['volume']))
        if self.sec_counter % config.time_scale2seconds['15m'] == 0: self.time_scales['15m'].enqueue(
            self.insert('15m', item['volume']))
        if self.sec_counter % config.time_scale2seconds['30m'] == 0: self.time_scales['30m'].enqueue(
            self.insert('30m', item['volume']))
        if self.sec_counter % config.time_scale2seconds['90m'] == 0: self.time_scales['90'].enqueue(
            self.insert('90m', item['volume']))
        if self.sec_counter % config.time_scale2seconds['1h'] == 0: self.time_scales['1h'].enqueue(
            self.insert('1h', item['volume']))
        if self.sec_counter % config.time_scale2seconds['1d'] == 0: self.time_scales['1d'].enqueue(
            self.insert('1d', item['volume']))
        if self.sec_counter % config.time_scale2seconds['5d'] == 0: self.time_scales['5d'].enqueue(
            self.insert('5d', item['volume']))
        if self.sec_counter % config.time_scale2seconds['1wk'] == 0: self.time_scales['1wk'].enqueue(
            self.insert('1wk', item['volume']))
        if self.sec_counter % config.time_scale2seconds['1mo'] == 0: self.time_scales['1mo'].enqueue(
            self.insert('1mo', item['volume']))
        if self.sec_counter % config.time_scale2seconds['3mo'] == 0: self.time_scales['3mo'].enqueue(
            self.insert('3mo', item['volume']))

        # initialize sec_counter to zero
        if self.sec_counter >= config.time_scale2seconds['3mo']: self.sec_counter = 0

    def insert(self, time_scale, volume):
        sec_dict = self.time_scales['1s']
        return {'open': sec_dict['open'][-config.time_scale2seconds[time_scale]],
                'low': min(sec_dict['low'][-config.time_scale2seconds[time_scale]:]),
                'high': max(sec_dict['high'][-config.time_scale2seconds[time_scale]:]),
                'close': sec_dict['close'][-1],
                'volume': volume}
