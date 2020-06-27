from libs.stocks.get_stock_info import GetStocksInfo
from libs.signal_generator.get_signal_info import GetSignalInfo
from libs.dataset.perceptron.dataset import DateSet
from libs.dl_models.dl_models import DLModels
from libs.callback.callback import CallBack
from libs.threading.threading import CustomTimer
import apps.ai.config as config
from tqdm import tqdm
from threading import Thread

prediction_type = config.prediction_type
window_size = config.window_size
stock_names = config.signal_names if config.TEST else config.stock_names

stocks_obj = GetSignalInfo() if config.TEST else GetStocksInfo()
callback = CallBack()
dl_models_obj = DLModels(config.prediction_type, callback)

for i in tqdm(range(config.window_size + 10 ** 3)):
    m = CustomTimer(1.0, stocks_obj.measure)
    m.start()
    m.join()

    for time_scale in config.time_scales:
        trainX, trainY, testX, testY = DateSet(stock_names).dataset_handler(time_scale, stocks_obj, dl_models_obj)

        # todo: this only works for MANY2ONE becuse of config.signal_name[0]
        stock_monitor = stocks_obj.stocks[stock_names[0]]['stock_obj'].time_scales[time_scale]



        dl_models_obj.fit(time_scale, trainX, trainY, testX, testY)

        if stocks_obj.ticks % config.time_scale2seconds[time_scale] == 0:
            thread = Thread(target=dl_models_obj.send2wandb(time_scale, trainX, trainY, testX, testY, stock_monitor))
            thread.start()
            thread.join()
