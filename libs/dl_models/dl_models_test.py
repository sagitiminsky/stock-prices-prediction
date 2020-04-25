import unittest
from unittest.mock import Mock
from libs.dl_models.dl_models import DLModels
import numpy as np

class StockRnnUnitTests(unittest.TestCase):
    def setUp(self):
        self.window_size = 20 # if you change this, change trainX,...,testY accordingly
        self.config = {
            'perceptron': {'lib': 'Keras', 'path2model': 'libs/dl_models/models_lib/perceptron/model', 'version': 'v_1',
                           'path2onnx_model': 'libs/dl_models/models_lib/perceptron/onnx'}}

        self.trainX=np.array([[[0], [0],[0],[0],[0],[0],[0]]])
        self.trainY=np.array([[0, 0, 0]])
        self.testX=np.array([[[0], [0],[0],[0],[0],[0],[0]]])
        self.testY = np.array([[0, 0, 0]])

    def test_perceptron(self):

        self.assertTrue(DLModels(window_size=self.window_size,config=self.config))

    def test_fit(self):
        dl_models=DLModels(window_size=self.window_size, config=self.config)
        dl_models.fit(trainX=self.trainX,trainY=self.trainY,testX=self.testX,testY=self.testY,callback=Mock())


if __name__ == '__main__':
    unittest.main()


