import numpy as np
from libs.stocks.queues.queue.queue import Queue


def pre_process(queue_obj, split):
    # split train and test data

    instance = isinstance(queue_obj, Queue)

    if instance:  # is Queue
        train = np.array(list(queue_obj._norm_queue)[:split])
        test = np.array(list(queue_obj._norm_queue)[split:])

    else:  # is QueueObejct
        dataset = queue_obj.get_vstacked_queues() #returned ndarray
        train = dataset[:, :split]
        test = dataset[:, split:]

    trainX, trainY = load_dataset(train, split, instance)
    testX, testY = load_dataset(test, split, instance)

    return (trainX, trainY, testX, testY)


def load_dataset(dataset, dataset_window, instance):
    first_values = int(dataset_window * 0.7)
    last_values = -int(dataset_window * 0.3)
    if instance:
        dataX = dataset[:first_values]
        dataY = dataset[last_values:]
    else:
        dataX = dataset[:, :first_values]
        dataY = dataset[:, last_values:]

    return dataX, dataY
