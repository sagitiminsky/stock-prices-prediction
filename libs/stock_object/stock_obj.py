from collections import deque
from libs.stock_object.graphs.graphs import Graphs

class StockObj():
    '''
    Thread-safe, memory-efficient, maximally-sized queue supporting queueing and
    dequeueing in worst-case O(1) time.
    '''



    def __init__(self,stock_name, max_size = 20):
        '''
        Initialize this queue to the empty queue.

        Parameters
        ----------
        max_size : int
            Maximum number of items contained in this queue. Defaults to 10.
        '''


        # sliding window - scraped stock values
        self._queue = deque(maxlen=max_size)
        self._norm_queue = deque(maxlen=max_size)
        self._max = None
        self._min = None

        # graphs - scraped
        self.graphs=Graphs(stock_name=stock_name)




    def enqueue(self, item):
        '''
        Queues the passed item (i.e., pushes this item onto the tail of this
        queue).

        If this queue is already full, the item at the head of this queue
        is silently removed from this queue *before* the passed item is
        queued.
        '''


        self._queue.append(item)
        self._max=max(self._queue)
        self._min=min(self._queue)

        try:
            self._norm_queue.append((item-self._min)/(self._max-self._min))
        except ZeroDivisionError:
            self._norm_queue.append(0)
        except TypeError: # item=Mock() object from unittest
            self._norm_queue.append(item)

    def dequeue(self):
        '''
        Dequeues (i.e., removes) the item at the head of this queue *and*
        returns this item from _queue and _norm_queue

        Raises
        ----------
        IndexError
            If this queue is empty.
        '''

        return (self._queue.pop(),self._norm_queue.pop())

