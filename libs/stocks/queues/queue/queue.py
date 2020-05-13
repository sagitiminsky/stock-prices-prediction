from collections import deque
import numpy as np

class Queue():
    '''
    Thread-safe, memory-efficient, maximally-sized queue supporting queueing and
    dequeueing in worst-case O(1) time.
    '''



    def __init__(self,init_list,maxlen):
        '''
        Initialize this queue to the empty queue.

        Parameters
        ----------
        max_size : int
            Maximum number of items contained in this queue. Defaults to 20.
        '''

        #filter out None values


        init_list_ex_None=[i for i in init_list if i!=None]
        self._queue = deque(init_list_ex_None,maxlen=maxlen)

        if self._queue!=deque([],maxlen=maxlen):
            self._max=max(init_list_ex_None)
            self._min = min(init_list_ex_None)
            self._norm_queue = self.normalize(init_list=init_list_ex_None, max=self._max, min=self._min, maxlen=maxlen)
        else:
            self._max=None
            self._min=None
            self._norm_queue=deque([],maxlen=maxlen)





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
        self._min = min(self._queue)


        try:
            self._norm_queue.append((item-self._min)/(self._max-self._min))
        except ZeroDivisionError:
            self._norm_queue.append(0)
        except (ValueError,TypeError): # item=Mock() object from unittest
            self._norm_queue.append(item)

    def normalize(self, init_list, max, min,maxlen):
        """
        Given a list of floats and min,max values, turn list to numpy array and normalize between 0 and 1
        :return: return collections.deuque of this transformation
        """

        np_array = np.array(init_list)
        try:
            return deque(np.nan_to_num((np_array - min) / (max - min)), maxlen=maxlen)
        except ZeroDivisionError:
            return deque(np.zeros(len(init_list)),maxlen=maxlen)