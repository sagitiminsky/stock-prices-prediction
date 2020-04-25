from keras.models import Sequential
from keras.layers import Dense, Flatten
from .dl_model import DLModel

from libs.callback.callback import CallBack

class DLModels:
    def __init__(self,window_size,config):
        self.window_size=window_size
        self.split=int(window_size*0.5)
        self.perceptron=DLModel(self.perceptron_init(),config['perceptron'])


    def perceptron_init(self):
        model = Sequential(name="Perceptron_stock_prediction")
        model.add(Flatten(input_shape=(int(self.split * 0.7), 1)))
        model.add(Dense(int(self.split * 0.3), name="output"))
        model.compile(loss='mse', optimizer='adam')
        return model

    def fit(self,trainX,trainY,testX,testY,callback):
        self.perceptron.model.fit(trainX, trainY, epochs=2, batch_size=10, validation_data=(testX, testY),
                                       callbacks=[callback.wandb,
                                                    callback.plot_callback(self.perceptron.model, trainX, trainY, testX, testY,self.window_size)])