#export PYTHONPATH=$PYTHON_PATH:/Users/sagit/Desktop/stock_price_prediction

######### STOCK OBJECT #######
max_window_size = {
    '1s': 900,  # 15 minutes at least (this means 900)
    '1m': 100,   # has to be same value for all (less then 100)
    '2m': 100,
    '5m': 100,
    '15m': 100,
    '30m': 100,
    '1h': 100,
    '1d': 100,
    '5d': 100,
    '1mo': 100,
    '3mo': 35
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
TEST=True
stock_names = ['FB', 'WMT']
signal_names = ['sin', 'cos']
window_size = max_window_size['1s']
prediction_type = MANY2ONE
callback = 10

DL_config = {'prediction_type': prediction_type,
             'stock_names': stock_names,
             'perceptron': {'lib': 'Keras', 'path2model': 'libs/dl_models/models_lib/perceptron/model',
                            'version': 'v_1',
                            'path2onnx_model': 'libs/dl_models/models_lib/perceptron/onnx'}}


######## GRAPHS #############
time_scales = ['1s', '1m', '2m', '5m', '15m', '30m', '1h', '1d', '5d', '1mo', '3mo']

url = "https://query1.finance.yahoo.com/v8/finance/chart/%s?symbol=%s&period1=%s&period2=%s&interval=%s&includePrePost=true"

TWO_MONTH = 5259492  # two month in seconds
A_WEEK = 604800  # a week in seconds
