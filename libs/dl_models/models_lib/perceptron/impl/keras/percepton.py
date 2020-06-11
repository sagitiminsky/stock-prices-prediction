import apps.ai.config as config
from keras.models import Sequential
from keras.layers import Dense, Flatten
class Perceptron:
    def __init__(self, time_scale):
        stocks_num = len(self.stock_names)

        # model
        model = Sequential(name="Perceptron_stock_prediction_of_" + time_scale)

        # input layer
        if time_scale == '1s':
            model.add(Flatten(input_shape=(stocks_num, int(int(config.max_window_size[time_scale] * 0.5) * 0.7))))
        else:  # open,low,high,close,volume
            model.add(Flatten(input_shape=(stocks_num, 5, int(int(config.max_window_size[time_scale] * 0.5) * 0.7))))

        # output layer

        # MANY2ONE
        if self.prediction_type == config.MANY2ONE:
            if time_scale == '1s':
                model.add(Dense(int(int(config.max_window_size[time_scale] * 0.5) * 0.3)))
            else:  # open,low,high,close,volume
                model.add(Dense(5 * int(int(config.max_window_size[time_scale] * 0.5) * 0.3)))
                # todo: in this case the output needs to be reshaped to (5,<prediction size>)

        # MANY2MANY
        else:
            if time_scale == '1s':
                model.add(Dense(int(int(config.max_window_size[time_scale] * 0.5) * 0.3) * stocks_num))
                # todo: in this case the output needs to be reshaped to (stocks_num,<prediction size>,)
            else:  # open,low,high,close,volume
                model.add(Dense(5 * int(int(config.max_window_size[time_scale] * 0.5) * 0.3) * stocks_num))
                # todo: in this case the output needs to be reshaped to (5,<prediction size>,stocks_num)

        model.compile(loss='mse', optimizer='adam')