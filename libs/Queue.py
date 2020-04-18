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
        self._maxlen=max_size
        self._maxValue = None
        self._minValue = None

    def normalize(self,queue,min,max):
        '''
        Normaliaze the window data between 0 and 1
        :return: Normalized window
        '''
        norm=[]
        for x in queue:
            try:
                norm.append((x-min)/(max-min))
            except ZeroDivisionError:
                norm.append(0)

        self._queue=deque(norm,maxlen=self._maxlen)


    def enqueue(self, item):
        '''
        Queues the passed item (i.e., pushes this item onto the tail of this
        queue).

        If this queue is already full, the item at the head of this queue
        is silently removed from this queue *before* the passed item is
        queued.
        '''

        self._queue.append(item)
        self._maxValue = max([x for x in self._queue])
        self._minValue = min([x for x in self._queue])

    def dequeue(self):
        '''
        Dequeues (i.e., removes) the item at the head of this queue *and*
        returns this item.

        Raises
        ----------
        IndexError
            If this queue is empty.
        '''

        ret=self._queue.pop()
        self._maxValue = max([x for x in self._queue])
        self._minValue = min([x for x in self._queue])

        return ret
