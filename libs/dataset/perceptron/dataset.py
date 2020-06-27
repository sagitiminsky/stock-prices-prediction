import numpy as np
from libs.stocks.queues.queue.queue import Queue
import apps.ai.config as config


class DateSet:
    def __init__(self,stock_names):
        self.trainX_s = None
        self.trainY_s = None
        self.testX_s = None
        self.testY_s = None
        self.stock_names=stock_names #could be signal_names

    def dataset_handler(self,  time_scale,stocks_obj,dl_models_obj):

        for stock_name in self.stock_names:
            batch = stocks_obj.stocks[stock_name]['stock_obj'].time_scales[time_scale]  # Queue or Candle

            trainX, trainY, testX, testY = self.pre_process(batch, int(config.max_window_size[time_scale] * 0.5))

            self.trainX_s, self.testX_s, self.trainY_s, self.testY_s = self.stack_dataset(self.trainX_s,
                                                                                          self.testX_s,
                                                                                          self.trainY_s,
                                                                                          self.testY_s,
                                                                                          trainX,
                                                                                          testX,
                                                                                          trainY,
                                                                                          testY,
                                                                                          time_scale)

        # reshape
        trainX = self.trainX_s[np.newaxis, :, :]
        testX = self.testX_s[np.newaxis, :, :]
        trainY = self.trainY_s[np.newaxis, :]
        testY = self.testY_s[np.newaxis, :]

        return trainX,trainY,testX,testY



    def pre_process(self, queue_obj, split):
        # split train and test data

        instance = isinstance(queue_obj, Queue)

        if instance:  # is Queue
            train = np.array(list(queue_obj._norm_queue)[:split])
            test = np.array(list(queue_obj._norm_queue)[split:])

        else:  # is Candle
            dataset = queue_obj.get_vstacked_queues()  # returned ndarray
            train = dataset[:, :split]
            test = dataset[:, split:]

        trainX, trainY = self.load_dataset(train, split, instance)
        testX, testY = self.load_dataset(test, split, instance)

        return (trainX, trainY, testX, testY)

    def load_dataset(self, dataset, dataset_window, instance):
        first_values = int(dataset_window * 0.7)
        last_values = -int(dataset_window * 0.3)
        if instance:
            dataX = dataset[:first_values]
            dataY = dataset[last_values:]
        else:
            dataX = dataset[:, :first_values]
            dataY = dataset[:, last_values:]

        return dataX, dataY

    def stack_dataset(self, trainX_s, testX_s, trainY_s, testY_s, trainX, testX, trainY, testY, time_scale):
        if trainX_s is None:
            trainX_s, testX_s, = trainX, testX

            # MANY2ONE
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

        return trainX_s, testX_s, trainY_s, testY_s
