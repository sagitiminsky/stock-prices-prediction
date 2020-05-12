from libs.stocks.get_stock_info import GetStocksInfo
from libs.dataset.load_dataset import *
from libs.dl_models.dl_models import DLModels
from libs.callback.callback import CallBack
from libs.signal_generator.signal_generator import SignalGenerator
import apps.ai.config as config
from tqdm import tqdm

prediction_type = config.prediction_type
window_size = config.window_size
stock_names = config.stock_names if config.sin == False else config.signals_names

stocks_obj = GetStocksInfo() if config.sin == False else SignalGenerator()

dl_models_obj = DLModels()
callback = CallBack()

for i in tqdm(range(config.window_size + 10 ** 2)):
    stocks_obj.measure()

    for time_scale_index, time_scale in enumerate(config.time_scales):

        trainX_s, trainY_s, testX_s, testY_s = None, None, None, None

        for stock_name in stock_names:

            batch = stocks_obj.stocks[stock_name]['stock_obj'].time_scales[time_scale]  # Queue or QueueObj

            trainX, trainY, testX, testY = pre_process(batch, dl_models_obj.split)

            if trainX_s is None:
                trainX_s,testX_s,  = trainX,testX
                trainY_s,testY_s =trainY.T.reshape(-1), testY.T.reshape(-1)

            else:  # vstack for stocks

                if time_scale == '1s':
                    trainX_s = np.vstack((trainX_s, trainX))
                    testX_s = np.vstack((testX_s, testX))

                else:  # 1m,2m,5m...
                    trainX_s = np.stack((trainX_s, trainX), axis=0)
                    testX_s = np.stack((testX_s, testX), axis=0)

                if prediction_type == config.MANY2MANY:
                    trainY_s = np.vstack((trainY_s, trainY))
                    testY_s = np.vstack((testY_s, testY))

        dl_models_obj.fit(trainX=trainX_s, trainY=trainY_s, testX=testX_s, testY=testY_s, callback=callback, i=i,
                          time_scale_index=time_scale_index)

# dl_models_obj.save()
