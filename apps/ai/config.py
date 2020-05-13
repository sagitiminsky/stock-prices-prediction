######### STOCK OBJECT #######
max_window_size = {
    '1s': 900, # 15 minutes
    '1m': 60, # an hour
    '2m': 30, # an hour
    '5m': 12,  # an hour
    '15m': 32,  # a day
    '30m': 16,  # a day
    '1h': 8,  # 8 a day
    '1d': 30,  # a month
    '5d': 4,  # a month
    '1mo': 6,  # half a year
    '3mo': 4,  # a year
}
time_scale2seconds = {
    '1s': 1,
    '1m': 60,
    '2m': 120,
    '5m': 300,
    '15m': 900,
    '30m': 1800,
    '1h': 3600,
    '1d': 86400,
    '5d': 432000,
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
time_scales = ['1s', '1m', '2m', '5m', '15m', '30m', '1h', '1d', '5d', '1mo', '3mo']

url = "https://query1.finance.yahoo.com/v8/finance/chart/%s?symbol=%s&period1=%s&period2=%s&interval=%s&includePrePost=true"

TWO_MONTH = 5259492  # two month in seconds
A_WEEK = 604800  # a week in seconds
