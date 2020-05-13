import unittest
from unittest.mock import Mock
from libs.dl_models.dl_models import DLModels
import numpy as np
import apps.ai.config as config


class StockRnnUnitTests(unittest.TestCase):
    def setUp(self):
        input_samples_number = int(int(config.max_window_size['1s'] * 0.5) * 0.7)
        output_samples_number = int(int(config.max_window_size['1s'] * 0.5) * 0.3)

        trainX_1s = np.array([[0] * input_samples_number,
                              [0] * input_samples_number])  # FB + WMT

        trainX_other = np.array([[[0] * input_samples_number, [0] * input_samples_number, [0] * input_samples_number,
                                  [0] * input_samples_number, [0] * input_samples_number],
                                 [[0] * input_samples_number, [0] * input_samples_number, [0] * input_samples_number,
                                  [0] * input_samples_number, [0] * input_samples_number]])  # FB + WMT

        trainY_1s = np.array([0] * output_samples_number)  # FB ONLY in 1s

        trainY_other = np.array([0] * 5 * output_samples_number)  # FB ONLY in (1m,2m,5m,15m...)

        testX_1s = np.array([[0] * input_samples_number,
                             [0] * input_samples_number])  # FB + WMT

        testX_other = np.array([[[0] * input_samples_number, [0] * input_samples_number, [0] * input_samples_number,
                                 [0] * input_samples_number, [0] * input_samples_number],
                                [[0] * input_samples_number, [0] * input_samples_number, [0] * input_samples_number,
                                 [0] * input_samples_number, [0] * input_samples_number]])  # FB + WMT

        testY_1s = np.array([0] * output_samples_number)  # FB ONLY in 1s

        testY_other = np.array([0] * 5 * output_samples_number)  # FB ONLY in (1m,2m,5m,15m...)

        self._1s_test_MANY2ONE = trainX_1s, trainY_1s, testX_1s, testY_1s
        self._other_test_MANY2ONE = trainX_other, trainY_other, testX_other, testY_other

        # todo: add MANY2MANY

    def test_perceptron_many_2_one(self):
        self.assertTrue(DLModels())

    # def test_perceptron_many_2_many(self):
    #     self.assertTrue(DLModels())

    def test_fit_many_2_one(self):
        dl_models = DLModels()

        for time_scale_index in range(len(config.time_scales)):
            if time_scale_index == 0:
                trainX, trainY, testX, testY = self._1s_test_MANY2ONE
            else:
                trainX, trainY, testX, testY = self._other_test_MANY2ONE

            dl_models.fit(trainX=trainX, trainY=trainY, testX=testX, testY=testY, callback=Mock(),
                          time_scale_index=time_scale_index, stock_monitor=Mock())
        # dl_models.save()

    # def test_fit_many_2_many(self):
    #     dl_models = DLModels()
    #     trainX, trainY, testX, testY = get_test_dataset(prediction_type=config.MANY2MANY)
    #     [dl_models.fit(trainX=trainX, trainY=trainY, testX=testX, testY=testY, callback=Mock(),
    #                    time_scale_index=time_scale_index, stock_monitor=Mock()) for time_scale_index in
    #      range(len(config.time_scales))]
    #     # dl_models.save()


if __name__ == '__main__':
    unittest.main()
