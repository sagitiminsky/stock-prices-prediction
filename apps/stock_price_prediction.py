from libs.stock_object.get_stock_info import GetStocksInfo
from libs.dataset.load_dataset import *
from libs.dl_models.dl_models import DLModels
from libs.callback.callback import CallBack
import apps.config



prediction_type=apps.config.prediction_type
window_size=apps.config.window_size
stock_names=apps.config.stock_names

config={'prediction_type':prediction_type,
        'perceptron':{'lib':'Keras','path2model':'libs/dl_models/models_lib/perceptron/model','version':'v_1',
                      'path2onnx_model':'libs/dl_models/models_lib/perceptron/onnx'}}

stocks_obj=GetStocksInfo(window_size,stock_names)
dl_models=DLModels(window_size=window_size,config=config)
callback=CallBack()


for i in range(35):
    stocks_obj.measure_stock()
    batch = stocks_obj.stocks[stock_names[-1]]['queueObj']._norm_queue
    print(len(batch))
    if len(batch)==window_size:
        trainX_s, trainY_s, testX_s, testY_s=None,None,None,None
        for stock_name in stock_names:
            batch=stocks_obj.stocks[stock_name]['queueObj']._norm_queue
            trainX,trainY,testX,testY=pre_process(batch, dl_models.split)

            if trainX_s is None:
                trainX_s, trainY_s, testX_s, testY_s=trainX,trainY,testX,testY

            else: # vstack
                trainX_s = np.hstack((trainX_s, trainX))
                trainY_s = np.hstack((trainY_s, trainY))
                testX_s = np.hstack((testX_s, testX))
                testY_s = np.hstack((testY_s, testY))


        dl_models.fit(trainX_s,trainY_s,testX_s,testY_s,callback)






