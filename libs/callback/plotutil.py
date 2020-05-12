import matplotlib

matplotlib.use('Agg')  # noqa
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
from tensorflow import keras
import numpy as np
import wandb


def fig2data(fig):
    """
    @brief Convert a Matplotlib figure to a 4D numpy array with RGBA channels and return it
    @param fig a matplotlib figure
    @return a numpy 3D array of RGBA values
    """
    # draw the renderer
    fig.canvas.draw()

    # Get the RGBA buffer from the figure
    w, h = fig.canvas.get_width_height()
    buf = np.fromstring(fig.canvas.tostring_argb(), dtype=np.uint8)
    buf.shape = (w, h, 4)

    # canvas.tostring_argb give pixmap in ARGB mode. Roll the ALPHA channel to have it in RGBA mode
    buf = np.roll(buf, 3, axis=2)
    return buf


class PlotCallback(keras.callbacks.Callback):
    def __init__(self, model, trainX, trainY, testX, testY, stock_monitor):
        super().__init__()
        self.repeat_predictions = True
        self.model = model
        self.trainX = trainX
        self.trainY = trainY
        self.testX = testX
        self.testY = testY
        self.stock_monitor = stock_monitor  # from here you can gain access to _max and _min - when batch is Queue this is simple as batch._min
        # but when stock_monitor is Queue_obj this is harder

    def on_epoch_end(self, epoch, logs=None):
        if self.repeat_predictions:
            preds = self.model.predict(self.trainX)
        else:
            preds = self.model.predict(self.testX)

        # Generate a figure with matplotlib
        figure = matplotlib.pyplot.figure(figsize=(20, 20))
        plot = figure.add_subplot(111)

        plot.plot(self.inverse(self.trainY), color='blue')
        plot.plot(np.append(np.empty_like(self.trainY) * np.nan, self.inverse(self.testY)), color='red')
        plot.plot(np.append(np.empty_like(self.trainY) * np.nan, self.inverse(preds)), color='green')

        data = fig2data(figure)
        matplotlib.pyplot.close(figure)

        wandb.log({"image": wandb.Image(data)}, commit=False)

    def inverse(self, arr):
        return arr * (self.stock_monitor._max - self.stock_monitor._min) + self.stock_monitor._min
