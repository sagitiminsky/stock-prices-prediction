from libs.dl_models.models_lib.perceptron.impl.keras.percepton import Perceptron
import apps.ai.config as config
import threading


class DLModels:
    def __init__(self, prediction_type, callback=None):

        self.prediction_type = prediction_type
        self.stock_names = config.stock_names
        self.callback = callback

        if self.stock_names == None or len(self.stock_names) == 0:
            raise ('stock names are invalid')

        self.perceptrons = {}
        for time_scale in config.time_scales:
            self.perceptrons[time_scale] = Perceptron(time_scale, prediction_type)

    def send2wandb(self, time_scale,trainX,trainY,testX,testY,stock_monitor):

        self.perceptrons[time_scale].model.fit(trainX, trainY, epochs=1, batch_size=10,
                                               validation_data=(testX, testY), verbose=0,
                                               callbacks=[self.callback.wandb,
                                                          self.callback.plot_callback(
                                                              self.perceptrons[time_scale].model,
                                                              trainX, trainY, testX, testY,
                                                              stock_monitor, time_scale)])

    def fit(self, time_scale,trainX,trainY,testX,testY):
        epoches = 5
        self.perceptrons[time_scale].model.fit(trainX, trainY, epochs=epoches, batch_size=10,
                                               validation_data=(testX, testY), verbose=0)

