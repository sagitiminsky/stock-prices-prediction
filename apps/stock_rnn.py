import neptune
from libs.get_stock_info import GetStockInfo
from libs.load_dataset import *
import numpy as np


from tensorflow import keras
from keras.models import Sequential
from keras.layers import Dense, Flatten
from keras.layers import LSTM, SimpleRNN, Dropout
from keras.callbacks import LambdaCallback

# The init() function called this way assumes that
# NEPTUNE_API_TOKEN environment variable is defined.


# Define parameters
# PARAMS = {'decay_factor' : 0.5,
#           'n_iterations' : 117}

# Create experiment with defined parameters
# neptune.init('sagit/stocks_rnn')
# neptune.create_experiment (name='example_with_parameters',
#                           params=PARAMS)


##### wandb #####
import wandb
from wandb.keras import WandbCallback
wandb.init()

stocks=['FB']
window_size=20


stocksObj=GetStockInfo(window_size,stocks)

#model
split=int(window_size*0.7)
model = Sequential(name="Perceptron_stock_prediction")
model.add(Flatten(input_shape=(int(split*0.7),1 ),name="input"))
model.add(Dense(int(split*0.3),name="output"))
model.compile(loss='mse', optimizer='adam')


def get_batch():
    stocksObj.measure_stock()
    stock_name='FB'
    # print('norm_values',stock_name , stocksObj.stocks[stock_name]['queueObj']._norm_queue)
    norm_queue=stocksObj.stocks[stock_name]['queueObj']._norm_queue

    return norm_queue

def pre_process(norm_queue):

    # split train and test data
    train = list(norm_queue)[:split]
    test = list(norm_queue)[split:]

    trainX, trainY = load_dataset(train, split)
    testX, testY = load_dataset(test, split)

    trainX = trainX[:, :, np.newaxis]
    testX = testX[:, :, np.newaxis]

    return (trainX,trainY,testX,testY)

for i in range(25):
    batch=get_batch()
    if len(batch)==window_size:
        trainX, trainY, testX, testY=pre_process(batch)
        model.fit(trainX, trainY, epochs=2, batch_size=10,callbacks=[WandbCallback()])






