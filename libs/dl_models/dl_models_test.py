import unittest
from unittest.mock import Mock
from libs.dl_models.dl_models import DLModels
import numpy as np
import apps.ai.config as config


def get_test_dataset(prediction_type):
    if prediction_type== config.MANY2ONE:
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

    def test_perceptron_many_2_one(self):
        self.assertTrue(DLModels(window_size=self.window_size,prediction_type=config.MANY2ONE))

    def test_perceptron_many_2_many(self):
        self.assertTrue(DLModels(window_size=self.window_size,prediction_type=config.MANY2MANY))

    def test_fit_many_2_one(self):
        dl_models=DLModels(window_size=self.window_size,prediction_type=config.MANY2ONE)
        trainX, trainY, testX, testY=get_test_dataset(config.MANY2ONE)
        dl_models.fit(trainX=trainX,trainY=trainY,testX=testX,testY=testY,callback=Mock(),i=10)
        # dl_models.save()


    def test_fit_many_2_many(self):
        dl_models=DLModels(window_size=self.window_size,prediction_type=config.MANY2MANY)
        trainX, trainY, testX, testY=get_test_dataset(config.MANY2MANY)
        dl_models.fit(trainX=trainX,trainY=trainY,testX=testX,testY=testY,callback=Mock(),i=10)
        # dl_models.save()



if __name__ == '__main__':
    unittest.main()


