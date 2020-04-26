from keras.models import Sequential
from keras.layers import Dense, Flatten
from .dl_model import DLModel
from libs.dl_models.many_2_x.many_2_x import *


class DLModels:
    def __init__(self,window_size,config):
        self.prediction_type=config['prediction_type'] if 'prediction_type' in config else None

        if self.prediction_type==None:
            raise('Prediction type is Invalid')

        self.window_size=window_size
        self.split=int(window_size*0.5)
        self.perceptron=DLModel(self.perceptron_init(),config['perceptron'])


    def perceptron_init(self):
        model = Sequential(name="Perceptron_stock_prediction")
        model=many_2_x(self.prediction_type,model=model,split=self.split)
        return model



    def fit(self,trainX,trainY,testX,testY,callback):
        self.perceptron.model.fit(trainX, trainY, epochs=2, batch_size=10, validation_data=(testX, testY),
                                  callbacks=[callback.wandb,
                                             callback.plot_callback(self.perceptron.model, trainX, trainY, testX,
                                                                    testY, self.window_size)])

