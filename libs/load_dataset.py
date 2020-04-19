import numpy as np
def load_dataset(dataset,dataset_window=10):
    dataX, dataY = [], []
    for i in range(len(dataset)-dataset_window-1):
        a = dataset[i:(i+dataset_window)]
        dataX.append(a)
        dataY.append(dataset[i + dataset_window + 1])
    return np.array(dataX), np.array(dataY)