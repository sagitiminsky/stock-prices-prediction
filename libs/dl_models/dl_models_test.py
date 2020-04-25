import unittest
from unittest.mock import Mock
from libs.dl_models.dl_models import DLModels
from libs.callback.callback import CallBack

class StockRnnUnitTests(unittest.TestCase):
    def setUp(self):
        self.window_size = 20
        self.config = {
            'perceptron': {'lib': 'Keras', 'path2model': 'libs/dl_models/models_lib/perceptron/model', 'version': 'v_1',
                           'path2onnx_model': 'libs/dl_models/models_lib/perceptron/onnx'}}

    def test_perceptron(self):

        self.assertTrue(DLModels(window_size=self.window_size,config=self.config))

    def test_fit(self):
        dl_models=DLModels(window_size=self.window_size, config=self.config)
        dl_models.fit(trainX=Mock(),trainY=Mock(),testX=Mock(),testY=Mock,callback=CallBack())


if __name__ == '__main__':
    unittest.main()


