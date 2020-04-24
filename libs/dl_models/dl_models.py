from keras.models import Sequential
from keras.layers import Dense, Flatten
from .dl_model import DLModel

class DLModels:
    def __init__(self,window_size,config):
        self.split=int(window_size*0.5)
        self.perceptron=DLModel(self.perceptron_init(),config['perceptron'])


    def perceptron_init(self):
        model = Sequential(name="Perceptron_stock_prediction")
        model.add(Flatten(input_shape=(int(self.split * 0.7), 1)))
        model.add(Dense(int(self.split * 0.3), name="output"))
        model.compile(loss='mse', optimizer='adam')
        return model