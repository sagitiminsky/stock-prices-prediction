from libs.stocks.graphs.graphs import Graphs_Obj
from libs.stocks.queue.queue import Queue
import libs.stocks.stock_object.config


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

        self._1s = Queue(max_size=libs.stocks.stock_object.config.max_window_size['1s'])
        # todo: find a smarter check point - not 'close'
        self._1m = Queue(init_list=self.graphs_obj.graphs['1m']['close'],
                         max_size=libs.stocks.stock_object.config.max_window_size['1m'])
        self._2m = Queue(init_list=self.graphs_obj.graphs['2m']['close'],
                         max_size=libs.stocks.stock_object.config.max_window_size['2m'])
        self._5m = Queue(init_list=self.graphs_obj.graphs['5m']['close'],
                         max_size=libs.stocks.stock_object.config.max_window_size['5m'])
        self._15m = Queue(init_list=self.graphs_obj.graphs['15m']['close'],
                          max_size=libs.stocks.stock_object.config.max_window_size['15m'])
        self._30m = Queue(init_list=self.graphs_obj.graphs['30m']['close'],
                          max_size=libs.stocks.stock_object.config.max_window_size['30m'])
        self._60m = Queue(init_list=self.graphs_obj.graphs['60m']['close'],
                          max_size=libs.stocks.stock_object.config.max_window_size['60m'])
        self._90m = Queue(init_list=self.graphs_obj.graphs['90m']['close'],
                          max_size=libs.stocks.stock_object.config.max_window_size['90m'])
        self._1h = Queue(init_list=self.graphs_obj.graphs['1h']['close'],
                         max_size=libs.stocks.stock_object.config.max_window_size['1h'])
        self._1d = Queue(init_list=self.graphs_obj.graphs['1d']['close'],
                         max_size=libs.stocks.stock_object.config.max_window_size['1d'])
        self._5d = Queue(init_list=self.graphs_obj.graphs['5d']['close'],
                         max_size=libs.stocks.stock_object.config.max_window_size['5d'])
        self._1wk = Queue(init_list=self.graphs_obj.graphs['1wk']['close'],
                          max_size=libs.stocks.stock_object.config.max_window_size['1wk'])
        self._1mo = Queue(init_list=self.graphs_obj.graphs['1mo']['close'],
                          max_size=libs.stocks.stock_object.config.max_window_size['1mo'])
        self._3mo = Queue(init_list=self.graphs_obj.graphs['3mo']['close'],
                                max_size=libs.stocks.stock_object.config.max_window_size['3mo'])

    def enqueue(self, item):
        '''
        Queues the passed item (i.e., pushes this item onto the tail of this
        queue).

        If this queue is already full, the item at the head of this queue
        is silently removed from this queue *before* the passed item is
        queued.
        '''
        self._1s.enqueue(item)
        self.sec_counter = self.sec_counter + 1
        if self.sec_counter % libs.stocks.stock_object.config.time_scale2seconds['1m'] == 0: self._1m.enqueue(item)
        if self.sec_counter % libs.stocks.stock_object.config.time_scale2seconds['2m'] == 0: self._2m.enqueue(item)
        if self.sec_counter % libs.stocks.stock_object.config.time_scale2seconds['5m'] == 0: self._5m.enqueue(item)
        if self.sec_counter % libs.stocks.stock_object.config.time_scale2seconds['15m'] == 0: self._15m.enqueue(item)
        if self.sec_counter % libs.stocks.stock_object.config.time_scale2seconds['30m'] == 0: self._30m.enqueue(item)
        if self.sec_counter % libs.stocks.stock_object.config.time_scale2seconds['60m'] == 0: self._60m.enqueue(item)
        if self.sec_counter % libs.stocks.stock_object.config.time_scale2seconds['90m'] == 0: self._90m.enqueue(item)
        if self.sec_counter % libs.stocks.stock_object.config.time_scale2seconds['1h'] == 0: self._1h.enqueue(item)
        if self.sec_counter % libs.stocks.stock_object.config.time_scale2seconds['1d'] == 0: self._1d.enqueue(item)
        if self.sec_counter % libs.stocks.stock_object.config.time_scale2seconds['5d'] == 0: self._5d.enqueue(item)
        if self.sec_counter % libs.stocks.stock_object.config.time_scale2seconds['1wk'] == 0: self._1wk.enqueue(item)
        if self.sec_counter % libs.stocks.stock_object.config.time_scale2seconds['1mo'] == 0: self._1mo.enqueue(item)
        if self.sec_counter % libs.stocks.stock_object.config.time_scale2seconds['3mo'] == 0: self._3mo.enqueue(item)

        # initialize sec_counter to zero
        if self.sec_counter >= libs.stocks.stock_object.config.time_scale2seconds['3mo']: self.sec_counter = 0
