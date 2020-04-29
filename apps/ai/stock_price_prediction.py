from libs.stock_object.get_stock_info import GetStocksInfo
from libs.dataset.load_dataset import *
from libs.dl_models.dl_models import DLModels
from libs.callback.callback import CallBack
from libs.signal_generator.signal_generator import SignalGenerator
import apps.ai.config
import libs.signal_generator.config
from tqdm import tqdm



prediction_type= apps.ai.config.prediction_type
window_size= apps.ai.config.window_size
stock_names= apps.ai.config.stock_names if apps.ai.config.sin == False else libs.signal_generator.config.signals_names

config={'prediction_type':prediction_type,
        'stock_names': apps.ai.config.stock_names,
        'perceptron':{'lib':'Keras','path2model':'libs/dl_models/models_lib/perceptron/model','version':'v_1',
                      'path2onnx_model':'libs/dl_models/models_lib/perceptron/onnx'}}



stocks_obj=GetStocksInfo() if apps.ai.config.sin == False else SignalGenerator()

dl_models=DLModels(window_size=window_size,config=config)
callback=CallBack()


for i in tqdm(range(apps.ai.config.window_size + 10 ** 2)):
    stocks_obj.measure()
    batch = stocks_obj.stocks[stock_names[0]]['queueObj']._norm_queue if apps.ai.config.sin == False else stocks_obj.stocks[stock_names[0]]['y']._queue
    # print(len(batch))
    if len(batch)==window_size:
        trainX_s, trainY_s, testX_s, testY_s=None,None,None,None
        for stock_name in stock_names:
            batch = stocks_obj.stocks[stock_names[0]]['queueObj']._norm_queue if apps.ai.config.sin == False else stocks_obj.stocks[stock_names[0]]['y']._queue

            trainX,trainY,testX,testY=pre_process(batch, dl_models.split)

            if trainX_s is None:
                trainX_s, trainY_s, testX_s, testY_s=trainX,trainY,testX,testY

            else: # hstack
                trainX_s = np.hstack((trainX_s, trainX))
                testX_s = np.hstack((testX_s, testX))

                if apps.ai.config.prediction_type == 'MANY2MANY':
                    trainY_s = np.hstack((trainY_s, trainY))
                    testY_s = np.hstack((testY_s, testY))


        dl_models.fit(trainX_s,trainY_s,testX_s,testY_s,callback,i)


dl_models.save()




