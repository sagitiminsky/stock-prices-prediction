import numpy as np
from .dl_model import DLModel
from libs.dl_models.models_lib.perceptron.impl.keras.percepton import Perceptron
import apps.ai.config as config
import threading


class DLModels:
    def __init__(self, prediction_type):

        self.prediction_type = prediction_type
        self.stock_names = config.stock_names

        if self.stock_names == None or len(self.stock_names) == 0:
            raise ('stock names are invalid')

        self.perceptrons = [Perceptron(time_scale,prediction_type) for time_scale in config.time_scales]



    def send2wandb(self,time_scale_index,i,trainX,trainY,testX,testY,callback,stock_monitor,time_scale):

        self.perceptrons[time_scale_index].model.fit(trainX, trainY, epochs=1, batch_size=10,
                                                     validation_data=(testX, testY), verbose=0,
                                                     callbacks=[callback.wandb,
                                                                callback.plot_callback(
                                                                    self.perceptrons[time_scale_index].model,
                                                                    trainX, trainY, testX, testY,
                                                                    stock_monitor, time_scale)])

    def fit(self, trainX, trainY, testX, testY, callback, time_scale_index, time_scale, stock_monitor, i):
        epoches = 5

        self.perceptrons[time_scale_index].model.fit(trainX, trainY, epochs=epoches, batch_size=10,
                                                     validation_data=(testX, testY), verbose=0)

        if i!=-1 and self.prediction_type == config.MANY2ONE and i%100==0 : #when i is -1 this is test mode
            threading.Timer(1.0, self.send2wandb,[time_scale_index,i,trainX,trainY,testX,testY,callback,stock_monitor,time_scale]).start()

