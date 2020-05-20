import unittest
from unittest.mock import Mock
from libs.dl_models.dl_models import DLModels
import numpy as np
import apps.ai.config as config


class StockRnnUnitTests(unittest.TestCase):
    def setUp(self):
        input_samples_number = int(int(config.max_window_size['1s'] * 0.5) * 0.7)
        output_samples_number = int(int(config.max_window_size['1s'] * 0.5) * 0.3)
        number_of_stocks = 2

        ######## TRAIN ########

        trainX_1s = np.array([[0] * input_samples_number,
                              [0] * input_samples_number])  # FB + WMT

        trainX_other = np.array([[[0] * input_samples_number, [0] * input_samples_number, [0] * input_samples_number,
                                  [0] * input_samples_number, [0] * input_samples_number],
                                 [[0] * input_samples_number, [0] * input_samples_number, [0] * input_samples_number,
                                  [0] * input_samples_number, [0] * input_samples_number]])  # FB + WMT

        trainY_1s_MANY2ONE = np.array([0] * output_samples_number)  # FB ONLY in 1s

        trainY_1s_MANY2MANY = np.array([0] * number_of_stocks * output_samples_number)  # FB + WMT in 1s

        trainY_other_MANY2ONE = np.array([0] * 5 * output_samples_number)  # FB ONLY in (1m,2m,5m,15m...)

        trainY_other_MANY2MANY = np.array(
            [0] * 5 * output_samples_number * number_of_stocks)  # FB + WMY  in (1m,2m,5m,15m...)

        ####### TEST #########

        testX_1s = np.array([[0] * input_samples_number,
                             [0] * input_samples_number])  # FB + WMT

        testX_other = np.array([[[0] * input_samples_number, [0] * input_samples_number, [0] * input_samples_number,
                                 [0] * input_samples_number, [0] * input_samples_number],
                                [[0] * input_samples_number, [0] * input_samples_number, [0] * input_samples_number,
                                 [0] * input_samples_number, [0] * input_samples_number]])  # FB + WMT

        testY_1s_MANY2ONE = np.array([0] * output_samples_number)  # FB ONLY in 1s

        testY_1s_MANY2MANY = np.array([0] * number_of_stocks * output_samples_number)  # FB + WMT in 1s

        testY_other_MANY2ONE = np.array([0] * 5 * output_samples_number)  # FB ONLY in (1m,2m,5m,15m...)

        testY_other_MANY2MANY = np.array(
            [0] * 5 * output_samples_number * number_of_stocks)  # FB + WMY  in (1m,2m,5m,15m...)

        self._1s_test_MANY2ONE = trainX_1s, trainY_1s_MANY2ONE, testX_1s, testY_1s_MANY2ONE
        self._other_test_MANY2ONE = trainX_other, trainY_other_MANY2ONE, testX_other, testY_other_MANY2ONE

        self._1s_test_MANY2MANY = trainX_1s, trainY_1s_MANY2MANY, testX_1s, testY_1s_MANY2MANY
        self._other_test_MANY2MANY = trainX_other, trainY_other_MANY2MANY, testX_other, testY_other_MANY2MANY

    def test_perceptron_many_2_one(self):
        self.assertTrue(DLModels(prediction_type=config.MANY2ONE))

    def test_perceptron_many_2_many(self):
        self.assertTrue(DLModels(prediction_type=config.MANY2MANY))

    def test_fit_many_2_one(self):
        dl_models = DLModels(prediction_type=config.MANY2ONE)

        for time_scale_index in range(len(config.time_scales)):
            if time_scale_index == 0:
                trainX, trainY, testX, testY = self._1s_test_MANY2ONE
            else:
                trainX, trainY, testX, testY = self._other_test_MANY2ONE

            dl_models.fit(trainX=trainX, trainY=trainY, testX=testX, testY=testY, callback=Mock(),
                          time_scale_index=time_scale_index, stock_monitor=Mock(),i=-1)
        # dl_models.save()

    def test_fit_many_2_many(self):
        dl_models = DLModels(prediction_type=config.MANY2MANY)
        for time_scale_index in range(len(config.time_scales)):
            time_scale_index = 0
            if time_scale_index == 0:
                trainX, trainY, testX, testY = self._1s_test_MANY2MANY
            else:
                trainX, trainY, testX, testY = self._other_test_MANY2MANY

            dl_models.fit(trainX=trainX, trainY=trainY, testX=testX, testY=testY, callback=Mock(),
                          time_scale_index=time_scale_index, stock_monitor=Mock(),i=-1)
        # dl_models.save()


if __name__ == '__main__':
    unittest.main()
