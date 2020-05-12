######### STOCK OBJECT #######
max_window_size = {
    '1s': 20, # do not change this 3mo worth in seconds
    '1m': 20,
    '2m': 20,
    '5m': 20,
    '15m': 20,
    '30m': 20,
    '90m': 20,
    '1h': 20,
    '1d': 20,
    '5d': 20,
    '1wk': 20,
    '1mo': 20,
    '3mo': 20,
}
time_scale2seconds = {
    '1s': 1,
    '1m': 60,
    '2m': 120,
    '5m': 300,
    '15m': 900,
    '30m': 1800,
    '90m': 5400,
    '1h': 3600,
    '1d': 86400,
    '5d': 432000,
    '1wk': 604800,
    '1mo': 2592000,  # todo: depends which month
    '3mo': 7776000,
}

######### MAIN CONFIG #########
# export PYTHONPATH=$PYTHON_PATH:/Users/sagit/Desktop/stocks_price_prediction
MANY2ONE = True
MANY2MANY = False
stock_names = ['FB', 'WMT']
window_size = max_window_size['1s']
prediction_type = MANY2ONE
callback = 10
sin = False

DL_config = {'prediction_type': prediction_type,
             'stock_names': stock_names,
             'perceptron': {'lib': 'Keras', 'path2model': 'libs/dl_models/models_lib/perceptron/model',
                            'version': 'v_1',
                            'path2onnx_model': 'libs/dl_models/models_lib/perceptron/onnx'}}

####### SIGNAL GENERATOR ########
signals_names = ['sin', 'cos']
delta = 0.1

######## GRAPHS #############
time_scales = ['1s', '1m', '2m', '5m', '15m', '30m', '90m', '1h', '1d', '5d', '1wk', '1mo', '3mo']

url = "https://query1.finance.yahoo.com/v8/finance/chart/%s?symbol=%s&period1=%s&period2=%s&interval=%s&includePrePost=true"

TWO_MONTH = 5259492  # two month in seconds
A_WEEK = 604800  # a week in seconds
