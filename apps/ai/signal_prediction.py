from libs.signal_generator.get_signal_info import GetSignalInfo
from libs.dataset.load_dataset import *
from libs.dl_models.dl_models import DLModels
from libs.callback.callback import CallBack
import apps.ai.config as config
from tqdm import tqdm
import threading

prediction_type = config.prediction_type
window_size = config.window_size
signal_names = config.signal_names

signals_obj = GetSignalInfo()
dl_models_obj = DLModels(prediction_type=config.prediction_type)
callback = CallBack()


def measuer(): signals_obj.measure()


x = threading.Thread(target=measuer)
x.start()

for i in tqdm(range(config.window_size + 10 ** 3)):
    for time_scale_index, time_scale in enumerate(config.time_scales):

        # todo: this only works for MANY2ONE becuse of config.signal_name[0]
        stock_monitor = signals_obj.signals[config.signal_names[0]]['stock_obj'].time_scales[
            time_scale]  # Queue or QueueObj

        trainX_s, trainY_s, testX_s, testY_s = None, None, None, None

        for signal_name in signal_names:

            batch = signals_obj.signals[signal_name]['stock_obj'].time_scales[time_scale]  # Queue or Candle

            trainX, trainY, testX, testY = pre_process(batch, int(config.max_window_size[time_scale] * 0.5))

            if trainX_s is None:
                trainX_s, testX_s, = trainX, testX

                # This will be the output layer in case prediction_type=MANY2ONE
                trainY_s, testY_s = trainY.T.reshape(-1), testY.T.reshape(-1)

            else:  # stacking stocks
                if time_scale == '1s':
                    trainX_s = np.vstack((trainX_s, trainX))
                    testX_s = np.vstack((testX_s, testX))

                else:  # 1m,2m,5m...
                    trainX_s = np.stack((trainX_s, trainX), axis=0)
                    testX_s = np.stack((testX_s, testX), axis=0)

                # only output layer changes if prediction_type=MANY2MANY
                if prediction_type == config.MANY2MANY:
                    if time_scale == '1s':
                        trainY_s = np.hstack((trainY_s, trainY))
                        testY_s = np.hstack((testY_s, testY))
                    else:
                        trainY_s, testY_s = np.hstack((trainY_s, trainY.T.reshape(-1))), np.hstack(
                            (testY_s, testY.T.reshape(-1)))

        dl_models_obj.fit(trainX=trainX_s, trainY=trainY_s, testX=testX_s, testY=testY_s, callback=callback,
                          time_scale_index=time_scale_index, time_scale=time_scale, stock_monitor=stock_monitor, i=i)

# dl_models_obj.save()
