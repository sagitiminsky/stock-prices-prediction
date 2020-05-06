from libs.stocks.graphs.graphs import Graphs_Obj
from libs.stocks.queues.queue.queue import Queue
from libs.stocks.queues.queue_obj.queue_obj import QueueObejct
import apps.ai.config as config


class StockObj():
    '''
    Thread-safe, memory-efficient, maximally-sized queue supporting queueing and
    dequeueing in worst-case O(1) time.
    '''

    def __init__(self, stock_name):
        '''
        Initialize this queue to the empty queue.

        Parameters
        ----------
        max_size : int
            Maximum number of items contained in this queue. Defaults to 10.
        '''

        self.sec_counter = 0

        # graphs - scraped
        self.graphs_obj = Graphs_Obj(stock_name=stock_name)

        self._1s = Queue(max_size=config.max_window_size['1s'])
        # todo: find a smarter check point - not 'close'
        self._1m = QueueObejct(init_dict=self.graphs_obj.graphs['1m'], time_scale='1m')
        self._2m = QueueObejct(init_dict=self.graphs_obj.graphs['2m'], time_scale='2m')
        self._5m = QueueObejct(init_dict=self.graphs_obj.graphs['5m'], time_scale='5m')
        self._15m = QueueObejct(init_dict=self.graphs_obj.graphs['15m'], time_scale='15m')
        self._30m = QueueObejct(init_dict=self.graphs_obj.graphs['30m'], time_scale='30m')
        self._90m = QueueObejct(init_dict=self.graphs_obj.graphs['90m'], time_scale='90m')
        self._1h = QueueObejct(init_dict=self.graphs_obj.graphs['1h'], time_scale='1h')
        self._1d = QueueObejct(init_dict=self.graphs_obj.graphs['1d'], time_scale='1d')
        self._5d = QueueObejct(init_dict=self.graphs_obj.graphs['5d'], time_scale='5d')
        self._1wk = QueueObejct(init_dict=self.graphs_obj.graphs['1wk'], time_scale='1wk')
        self._1mo = QueueObejct(init_dict=self.graphs_obj.graphs['1mo'], time_scale='1mo')
        self._3mo = QueueObejct(init_dict=self.graphs_obj.graphs['3mo'], time_scale='3mo')

    def enqueue(self, item):
        '''
        Queues the passed item (i.e., pushes this item onto the tail of this
        queue).

        If this queue is already full, the item at the head of this queue
        is silently removed from this queue *before* the passed item is
        queued.
        '''
        self._1s.enqueue(item['value'])
        self.sec_counter = self.sec_counter + 1
        if self.sec_counter % config.time_scale2seconds['1m'] == 0: self._1m.enqueue(self.insert('1m',item['volume']))
        if self.sec_counter % config.time_scale2seconds['2m'] == 0: self._2m.enqueue(self.insert('2m',item['volume']))
        if self.sec_counter % config.time_scale2seconds['5m'] == 0: self._5m.enqueue(self.insert('5m',item['volume']))
        if self.sec_counter % config.time_scale2seconds['15m'] == 0: self._15m.enqueue(self.insert('15m',item['volume']))
        if self.sec_counter % config.time_scale2seconds['30m'] == 0: self._30m.enqueue(self.insert('30m',item['volume']))
        if self.sec_counter % config.time_scale2seconds['90m'] == 0: self._90m.enqueue(self.insert('90m',item['volume']))
        if self.sec_counter % config.time_scale2seconds['1h'] == 0: self._1h.enqueue(self.insert('1h',item['volume']))
        if self.sec_counter % config.time_scale2seconds['1d'] == 0: self._1d.enqueue(self.insert('1d',item['volume']))
        if self.sec_counter % config.time_scale2seconds['5d'] == 0: self._5d.enqueue(self.insert('5d',item['volume']))
        if self.sec_counter % config.time_scale2seconds['1wk'] == 0: self._1wk.enqueue(self.insert('1wk',item['volume']))
        if self.sec_counter % config.time_scale2seconds['1mo'] == 0: self._1mo.enqueue(self.insert('1mo',item['volume']))
        if self.sec_counter % config.time_scale2seconds['3mo'] == 0: self._3mo.enqueue(self.insert('3mo',item['volume']))

        # initialize sec_counter to zero
        if self.sec_counter >= config.time_scale2seconds['3mo']: self.sec_counter = 0

    def insert(self, time_scale,volume):
        sec_list = list(self._1s)
        return {'open': sec_list[-config.time_scale2seconds[time_scale]],
                'low': min(sec_list[-config.time_scale2seconds[time_scale]:]),
                'high': max(sec_list[-config.time_scale2seconds[time_scale]:]),
                'close': sec_list[-1],
                'volume':volume}
