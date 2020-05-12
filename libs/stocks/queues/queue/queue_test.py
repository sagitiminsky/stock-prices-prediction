import unittest
from libs.stocks.queues.queue.queue import Queue

class TestQueue(unittest.TestCase):
    def setUp(self):
        self.list=[1,2,3,4]
        self.insert_item=6
        self.maxlen=4


    def test_initialized_queue(self):
        self.assertTrue(Queue(init_list=self.list,maxlen=self.maxlen))

    def test_enque(self):
        q=Queue(init_list=self.list,maxlen=self.maxlen)
        q.enqueue(self.insert_item)
        self.assertTrue(q)

if __name__ == '__main__':
    unittest.main()


