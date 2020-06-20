import numpy as np
from libs.stocks.queues.queue.queue import Queue
import apps.ai.config as config

def pre_process(queue_obj, split):
    # split train and test data

    instance = isinstance(queue_obj, Queue)

    if instance:  # is Queue
        train = np.array(list(queue_obj._norm_queue)[:split])
        test = np.array(list(queue_obj._norm_queue)[split:])

    else:  # is Candle
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

def stack_dataset(trainX_s,testX_s,trainY_s,testY_s,trainX,testX,trainY,testY,time_scale):
    if trainX_s is None:
        trainX_s, testX_s, = trainX, testX

        #MANY2ONE
        trainY_s, testY_s = trainY.T.reshape(-1), testY.T.reshape(-1)

    else:  # stacking stocks
        if time_scale == '1s':
            trainX_s = np.vstack((trainX_s, trainX))
            testX_s = np.vstack((testX_s, testX))

        else:  # 1m,2m,5m...
            trainX_s = np.stack((trainX_s, trainX), axis=1).T
            testX_s = np.stack((testX_s, testX), axis=1).T

        # only output layer changes if prediction_type=MANY2MANY
        if config.prediction_type == config.MANY2MANY:
            if time_scale == '1s':
                trainY_s = np.hstack((trainY_s, trainY))
                testY_s = np.hstack((testY_s, testY))
            else:
                trainY_s, testY_s = np.hstack((trainY_s, trainY.T.reshape(-1))), np.hstack(
                    (testY_s, testY.T.reshape(-1)))


    return trainX_s,testX_s,trainY_s,testY_s