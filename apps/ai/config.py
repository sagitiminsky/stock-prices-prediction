import libs.stocks.stock_object.config
# export PYTHONPATH=$PYTHON_PATH:/Users/sagit/Desktop/stocks_price_prediction
MANY2ONE=True
MANY2MANY=False
stock_names=['FB','WMT']
window_size=libs.stocks.stock_object.config.max_window_size['1s']
prediction_type=MANY2MANY
callback=10
sin=True

