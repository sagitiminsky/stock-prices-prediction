import numpy as np
def load_dataset(dataset,dataset_window):
    dataX, dataY = [], []
    first_values=int(dataset_window*0.7)
    last_values=-int(dataset_window*0.3)
    a = dataset[:first_values]
    dataX.append(a)
    dataY.append(dataset[last_values:])
    return np.array(dataX), np.array(dataY)