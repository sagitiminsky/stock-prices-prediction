import apps.ai.config as config
from keras.models import Sequential
from keras.layers import Dense, Flatten
class Perceptron:
    def __init__(self, time_scale,prediction_type):

        stocks_num = len(config.stock_names)

        # model
        self.model = Sequential(name="Perceptron_stock_prediction_of_" + time_scale)

        # input layer
        if time_scale == '1s':
            self.model.add(Flatten(input_shape=(stocks_num, int(int(config.max_window_size[time_scale] * 0.5) * 0.7)),name=f'time_scale_{time_scale}'))
        else:  # open,low,high,close,volume
            self.model.add(Flatten(input_shape=(stocks_num, 5, int(int(config.max_window_size[time_scale] * 0.5) * 0.7)),name=f'time_scale_{time_scale}'))

        # output layer

        # MANY2ONE
        if prediction_type == config.MANY2ONE:
            if time_scale == '1s':
                self.model.add(Dense(int(int(config.max_window_size[time_scale] * 0.5) * 0.3)))
            else:  # open,low,high,close,volume | 5 x <prediction size>
                self.model.add(Dense(5 * int(int(config.max_window_size[time_scale] * 0.5) * 0.3)))


        # MANY2MANY
        else:
            if time_scale == '1s':# stock_type x <prediction size>
                self.model.add(Dense(int(int(config.max_window_size[time_scale] * 0.5) * 0.3) * stocks_num))

            else:  # open,low,high,close,volume | 5 x <prediction size> x <stock_type>
                self.model.add(Dense(5 * int(int(config.max_window_size[time_scale] * 0.5) * 0.3) * stocks_num))


        self.model.compile(loss='mse', optimizer='adam')