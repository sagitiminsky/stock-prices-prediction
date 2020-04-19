import neptune
from libs.get_stock_info import GetStockInfo
from libs.load_dataset import *



# The init() function called this way assumes that
# NEPTUNE_API_TOKEN environment variable is defined.


# Define parameters
# PARAMS = {'decay_factor' : 0.5,
#           'n_iterations' : 117}

# Create experiment with defined parameters
# neptune.init('sagit/stocks_rnn')
# neptune.create_experiment (name='example_with_parameters',
#                           params=PARAMS)

stocks=['FB']
window_size=20


stocksObj=GetStockInfo(window_size,stocks)


for i in range(window_size+5):
    stocksObj.measure_stock()
    for stock_name in stocks:
        print('norm_values',stock_name , stocksObj.stocks[stock_name]['queueObj']._norm_queue)
        norm_queue=stocksObj.stocks[stock_name]['queueObj']._norm_queue

        if i>=window_size:
            #split train and test data
            split=int(window_size*0.7)
            train=list(norm_queue)[:split]
            test=list(norm_queue)[split:]

            trainX, trainY = load_dataset(train,split//2)
            testX, testY = load_dataset(test,(window_size-split)//2)

            print('trainX',trainX)
            print('trainY',trainY)


