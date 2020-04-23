from keras.models import Sequential
from keras.layers import Dense, Flatten


class DLModels:
    def __init__(self,window_size):
        self.split=int(window_size*0.5)
        self.perceptron=self.perceptron_init()

    def perceptron_init(self):
        model = Sequential(name="Perceptron_stock_prediction")
        model.add(Flatten(input_shape=(int(self.split * 0.7), 1)))
        model.add(Dense(int(self.split * 0.3), name="output"))
        model.compile(loss='mse', optimizer='adam')
        return model