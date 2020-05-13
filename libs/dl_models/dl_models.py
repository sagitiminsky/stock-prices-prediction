from keras.models import Sequential
from keras.layers import Dense, Flatten
import numpy as np
from .dl_model import DLModel
import apps.ai.config as config


class DLModels:
    def __init__(self, prediction_type):

        self.prediction_type = prediction_type
        self.stock_names = config.stock_names

        if self.stock_names == None or len(self.stock_names) == 0:
            raise ('stock names are invalid')

        self.split = int(config.window_size * 0.5)

        self.perceptrons = [
            DLModel(self.perceptron_init(time_scale), config.DL_config['perceptron'], time_scale=time_scale) for
            time_scale in config.time_scales]

        self.models = [self.perceptrons]  ## ADD MORE MODELS HERE

    def perceptron_init(self, time_scale):
        stocks_num = len(self.stock_names)

        # model
        model = Sequential(name="Perceptron_stock_prediction_of_" + time_scale)

        # input layer
        if time_scale == '1s':
            model.add(Flatten(input_shape=(stocks_num, int(self.split * 0.7))))
        else:  # open,low,high,close,volume
            model.add(Flatten(input_shape=(stocks_num, 5, int(self.split * 0.7))))

        # output layer

        # MANY2ONE
        if self.prediction_type == config.MANY2ONE:
            if time_scale == '1s':
                model.add(Dense(int(self.split * 0.3)))
            else:  # open,low,high,close,volume
                model.add(Dense(5 * int(self.split * 0.3)))
                # todo: in this case the output needs to be reshaped to (5,<prediction size>)

        # MANY2MANY
        else:
            if time_scale == '1s':
                model.add(Dense(int(self.split * 0.3) * stocks_num))
                # todo: in this case the output needs to be reshaped to (stocks_num,<prediction size>,)
            else:  # open,low,high,close,volume
                model.add(Dense(5 * int(self.split * 0.3) * stocks_num))
                # todo: in this case the output needs to be reshaped to (5,<prediction size>,stocks_num)

        model.compile(loss='mse', optimizer='adam')
        return model

    def fit(self, trainX, trainY, testX, testY, callback, time_scale_index, stock_monitor):
        epoches = 10

        # reshape
        trainX = trainX[np.newaxis, :, :]
        testX = testX[np.newaxis, :, :]
        trainY = trainY[np.newaxis, :]
        testY = testY[np.newaxis, :]

        self.perceptrons[time_scale_index].model.fit(trainX, trainY, epochs=epoches, batch_size=10,
                                                     validation_data=(testX, testY), verbose=0)

        ### ADD MORE MODELS HERE

        if time_scale_index == 0 and self.prediction_type == config.MANY2ONE:  # todo: do for all time_scales and for MANY2MANY as well
            self.perceptrons[time_scale_index].model.fit(trainX, trainY, epochs=1, batch_size=10,
                                                         validation_data=(testX, testY), verbose=0,
                                                         callbacks=[callback.wandb,
                                                                    callback.plot_callback(
                                                                        self.perceptrons[time_scale_index].model,
                                                                        trainX, trainY, testX, testY,
                                                                        stock_monitor)])
        ### ADD MORE MODELS HERE TO SEE THEM IN WANDB

    def save(self):
        for model in self.models:
            for time_scale_model in model:
                time_scale_model.export_model()
                time_scale_model.export_onnx_model()
