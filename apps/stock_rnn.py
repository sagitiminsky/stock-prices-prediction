import neptune
from libs.get_stock_info import GetStockInfo




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
window_size=10
stocksObj=GetStockInfo(window_size,stocks)


for i in range(15):
    stocksObj.measure_stock()
    for stock_name in stocks:
        print('norm_values',stock_name , stocksObj.stocks[stock_name]['norm_values'].__dict__)


