#!/usr/bin/env sh
#export PYTHONPATH=$PYTHON_PATH:/Users/sagit/Desktop/stocks_RNN
pytest libs/stock_object/get_stock_info_test.py
pytest libs/dl_models/dl_models_test.py
pytest libs/callback/callback_test.py
