import unittest
from unittest.mock import Mock
from libs.dl_models.dl_models import DLModels
import numpy as np
import apps.ai.config

def get_tets_dataset(prediction_type):
    if prediction_type== apps.ai.config.MANY2ONE:
        trainX = np.array([[[0], [0], [0], [0], [0], [0], [0] , [0], [0], [0], [0], [0], [0], [0]]]) # FB + WMT
        trainY = np.array([[0, 0, 0]]) #FB ONLY
        testX = np.array([[[0], [0], [0], [0], [0], [0], [0] ,[0], [0], [0], [0], [0], [0], [0]]]) #FB + WMT
        testY = np.array([[0, 0, 0]]) # FB ONLY

    else: # MANY2MANY
        trainX = np.array([[[0], [0], [0], [0], [0], [0], [0] , [0], [0], [0], [0], [0], [0], [0]]]) # FB + WMT
        trainY = np.array([[0, 0, 0 ,0, 0, 0]]) # FB + WMT
        testX = np.array([[[0], [0], [0], [0], [0], [0], [0] ,[0], [0], [0], [0], [0], [0], [0]]]) # FB + WMT
        testY = np.array([[0, 0, 0 ,0, 0, 0]]) # FB + WMT

    return trainX,trainY,testX,testY

class StockRnnUnitTests(unittest.TestCase):
    def setUp(self):
        self.window_size = 20 # if you change this, change trainX,...,testY accordingly

        self.config = {'prediction_type': None,
                       'stock_names': apps.ai.config.stock_names,
                  'perceptron': {'lib': 'Keras', 'path2model': 'libs/dl_models/models_lib/perceptron/model',
                                 'version': 'v_1',
                                 'path2onnx_model': 'libs/dl_models/models_lib/perceptron/onnx'}}

    def test_perceptron_many_2_one(self):
        self.config['prediction_type']= apps.ai.config.MANY2ONE
        self.assertTrue(DLModels(window_size=self.window_size,config=self.config))

    def test_perceptron_many_2_many(self):
        self.config['prediction_type']= apps.ai.config.MANY2MANY
        self.assertTrue(DLModels(window_size=self.window_size,config=self.config))

    def test_fit_many_2_one(self):
        self.config['prediction_type'] = apps.ai.config.MANY2ONE
        dl_models=DLModels(window_size=self.window_size, config=self.config)
        trainX, trainY, testX, testY=get_tets_dataset(apps.ai.config.MANY2ONE)
        dl_models.fit(trainX=trainX,trainY=trainY,testX=testX,testY=testY,callback=Mock())


    def test_fit_many_2_many(self):
        self.config['prediction_type'] = apps.ai.config.MANY2MANY
        dl_models=DLModels(window_size=self.window_size, config=self.config)
        trainX, trainY, testX, testY=get_tets_dataset(apps.ai.config.MANY2MANY)
        dl_models.fit(trainX=trainX,trainY=trainY,testX=testX,testY=testY,callback=Mock())



if __name__ == '__main__':
    unittest.main()


