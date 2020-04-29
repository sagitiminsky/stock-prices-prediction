from keras.models import Sequential
from keras.layers import Dense, Flatten
from .dl_model import DLModel
import apps.config


class DLModels:
    def __init__(self,window_size,config):
        self.prediction_type=config['prediction_type'] if 'prediction_type' in config else None

        if self.prediction_type==None:
            raise('Prediction type is Invalid')

        self.stock_names=config['stock_names'] if 'stock_names' in config else None

        if self.stock_names==None or len(self.stock_names)==0:
            raise ('stock names are invalid')

        self.window_size=window_size
        self.split=int(window_size*0.5)

        self.perceptron=DLModel(self.perceptron_init(),config['perceptron'])


    def perceptron_init(self):
        stocks_num = len(self.stock_names)

        #model
        model = Sequential(name="Perceptron_stock_prediction")
        model.add(Flatten(input_shape=(int(self.split * 0.7) * stocks_num, 1), name="perceptron"))
        if self.prediction_type == apps.config.MANY2MANY: #MANY2MANY
            model.add(Dense(int(self.split * 0.3) * stocks_num, name="output"))
        else: #MANY2ONE
            model.add(Dense(int(self.split * 0.3), name="output"))
        model.compile(loss='mse', optimizer='adam')
        return model



    def fit(self,trainX,trainY,testX,testY,callback,i):
        epoches=10
        if i%apps.config.callback==0:
            self.perceptron.model.fit(trainX, trainY, epochs=epoches, batch_size=10, validation_data=(testX, testY),verbose=0,
                                      callbacks=[callback.wandb,
                                                 callback.plot_callback(self.perceptron.model, trainX, trainY, testX,testY, self.window_size)])
        else:
            self.perceptron.model.fit(trainX, trainY, epochs=epoches, batch_size=10, validation_data=(testX, testY),verbose=0)
