import numpy as np


def pre_process(norm_queue,split):

    # split train and test data
    train = list(norm_queue)[:split]
    test = list(norm_queue)[split:]

    trainX, trainY = load_dataset(train, split)
    testX, testY = load_dataset(test, split)

    trainX = trainX[:, :, np.newaxis]
    testX = testX[:, :, np.newaxis]

    return (trainX,trainY,testX,testY)


def load_dataset(dataset,dataset_window):
    dataX, dataY = [], []
    first_values=int(dataset_window*0.7)
    last_values=-int(dataset_window*0.3)
    a = dataset[:first_values]
    dataX.append(a)
    dataY.append(dataset[last_values:])
    return np.array(dataX), np.array(dataY)