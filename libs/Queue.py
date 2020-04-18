from collections import deque

class Queue():
    '''
    Thread-safe, memory-efficient, maximally-sized queue supporting queueing and
    dequeueing in worst-case O(1) time.
    '''



    def __init__(self, max_size = 10):
        '''
        Initialize this queue to the empty queue.

        Parameters
        ----------
        max_size : int
            Maximum number of items contained in this queue. Defaults to 10.
        '''

        self._queue = deque(maxlen=max_size)
        self._norm_queue = deque(maxlen=max_size)
        self._max = None
        self._min = None



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

    def dequeue(self):
        '''
        Dequeues (i.e., removes) the item at the head of this queue *and*
        returns this item.

        Raises
        ----------
        IndexError
            If this queue is empty.
        '''

        self._queue.pop()
        self._norm_queue.pop()
