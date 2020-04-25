from libs.stock_object.get_stock_info import GetStockInfo
from libs.dataset.load_dataset import *
from libs.dl_models.dl_models import DLModels
from libs.callback.callback import CallBack



# The init() function called this way assumes that
# NEPTUNE_API_TOKEN environment variable is defined.


# Define parameters
# PARAMS = {'decay_factor' : 0.5,
#           'n_iterations' : 117}

# Create experiment with defined parameters
# neptune.init('sagit/stocks_rnn')
# neptune.create_experiment (name='example_with_parameters',
#                           params=PARAMS)


##### wandb #####




wandb.init()

stock_names=['FB']
window_size=20


config={'perceptron':{'lib':'Keras','path2model':'libs/dl_models/models_lib/perceptron/model','version':'v_1',
                      'path2onnx_model':'libs/dl_models/models_lib/perceptron/onnx'}}

stocks_obj=GetStockInfo(window_size,stock_names)
dl_models=DLModels(window_size)
callback=CallBack()


for i in range(35):
    stocks_obj.measure_stock()
    batch=stocks_obj.stocks[stock_names[0]]['queueObj']._norm_queue
    print(len(batch))
    if len(batch)==window_size:
        trainX, trainY, testX, testY=pre_process(batch,dl_models.split)
        dl_models.fit(trainX,trainY,testX,testY,callback)






