import unittest
from unittest.mock import Mock
from libs.dl_models.dl_models import DLModels
import numpy as np
import apps.ai.config as config


def get_dataset(prediction_type, time_scale):
    ins_number = int(int(config.max_window_size[time_scale] * 0.5) * 0.7)
    outs_number = int(int(config.max_window_size[time_scale] * 0.5) * 0.3)
    number_of_stocks = len(config.signal_names) if config.TEST else len(config.stock_names)

    ######## TRAIN ########

    trainX_1s = np.array([[0] * ins_number] * number_of_stocks)

    trainX_other = np.array([[[0] * 5] * number_of_stocks] * ins_number)

    trainY_1s_MANY2ONE = np.array([0] * outs_number)

    trainY_1s_MANY2MANY = np.array([0] * number_of_stocks * outs_number)

    trainY_other_MANY2ONE = np.array([0] * 5 * outs_number)

    trainY_other_MANY2MANY = np.array([0] * number_of_stocks * 5 * outs_number)

    ####### TEST #########

    testX_1s = np.array([[0] * ins_number] * number_of_stocks)

    testX_other = np.array([[[0] * 5] * number_of_stocks] * ins_number)

    testY_1s_MANY2ONE = np.array([0] * outs_number)

    testY_1s_MANY2MANY = np.array([0] * number_of_stocks * outs_number)

    testY_other_MANY2ONE = np.array([0] * 5 * outs_number)

    testY_other_MANY2MANY = np.array([0] * number_of_stocks * 5 * outs_number)

    if prediction_type == config.MANY2ONE and time_scale == '1s':
        return trainX_1s, trainY_1s_MANY2ONE, testX_1s, testY_1s_MANY2ONE

    elif prediction_type == config.MANY2ONE and time_scale != '1s':
        return trainX_other, trainY_other_MANY2ONE, testX_other, testY_other_MANY2ONE

    elif prediction_type == config.MANY2MANY and time_scale == '1s':
        return trainX_1s, trainY_1s_MANY2MANY, testX_1s, testY_1s_MANY2MANY

    elif prediction_type == config.MANY2MANY and time_scale != '1s':
        return trainX_other, trainY_other_MANY2MANY, testX_other, testY_other_MANY2MANY

    else:
        raise Exception(f"prediction type: {prediction_type} or time_scale: {time_scale} are invalid")


class StockRnnUnitTests(unittest.TestCase):
    def test_perceptron_many_2_one(self):
        dl_models = DLModels(prediction_type=config.MANY2ONE)

        for time_scale_index, time_scale in enumerate(config.time_scales):
            trainX, trainY, testX, testY = get_dataset(config.MANY2ONE, time_scale)

            # reshape
            trainX = trainX[np.newaxis, :, :]
            testX = testX[np.newaxis, :, :]
            trainY = trainY[np.newaxis, :]
            testY = testY[np.newaxis, :]

            dl_models.fit(trainX=trainX, trainY=trainY, testX=testX, testY=testY,time_scale=time_scale)

    def test_perceptron_many_2_many(self):
        dl_models = DLModels(prediction_type=config.MANY2MANY)

        for time_scale_index, time_scale in enumerate(config.time_scales):
            trainX, trainY, testX, testY = get_dataset(config.MANY2MANY, time_scale)

            # reshape
            trainX = trainX[np.newaxis, :, :]
            testX = testX[np.newaxis, :, :]
            trainY = trainY[np.newaxis, :]
            testY = testY[np.newaxis, :]

            dl_models.fit(trainX=trainX, trainY=trainY, testX=testX, testY=testY, time_scale=time_scale)


if __name__ == '__main__':
    unittest.main()
