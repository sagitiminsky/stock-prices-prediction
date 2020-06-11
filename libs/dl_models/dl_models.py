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

        self.perceptrons = [
            DLModel(Perceptron(time_scale), config.DL_config['perceptron'], time_scale=time_scale) for
            time_scale in config.time_scales]

        self.models = [self.perceptrons]  ## ADD MORE MODELS HERE


    def send2wandb(self,time_scale_index,i,trainX,trainY,testX,testY,callback,stock_monitor,time_scale):

        for model in self.models:
            model[time_scale_index].model.fit(trainX, trainY, epochs=1, batch_size=10,
                                                         validation_data=(testX, testY), verbose=0,
                                                         callbacks=[callback.wandb,
                                                                    callback.plot_callback(
                                                                        model[time_scale_index].model,
                                                                        trainX, trainY, testX, testY,
                                                                        stock_monitor, time_scale)])

    def fit(self, trainX, trainY, testX, testY, callback, time_scale_index, time_scale, stock_monitor, i):
        epoches = 100

        # reshape
        trainX = trainX[np.newaxis, :, :]
        testX = testX[np.newaxis, :, :]
        trainY = trainY[np.newaxis, :]
        testY = testY[np.newaxis, :]

        for model in self.models:
            model[time_scale_index].model.fit(trainX, trainY, epochs=epoches, batch_size=10,
                                                         validation_data=(testX, testY), verbose=0)

        if self.prediction_type == config.MANY2ONE:  # todo:  MANY2MANY as well
            threading.Timer(1.0, self.send2wandb,[time_scale_index,i,trainX,trainY,testX,testY,callback,stock_monitor,time_scale]).start()

    def save(self):
        for model in self.models:
            for time_scale_model in model:
                time_scale_model.export_model()
                time_scale_model.export_onnx_model()
