import matplotlib

matplotlib.use('Agg')  # noqa
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
from tensorflow import keras
import numpy as np
import wandb
import plotly.graph_objs as go
from PIL import Image as PILImage


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
    def __init__(self, model, trainX, trainY, testX, testY, stock_monitor, time_scale):
        super().__init__()
        self.repeat_predictions = True
        self.model = model
        self.trainX = trainX
        self.trainY = trainY
        self.testX = testX
        self.testY = testY
        self.stock_monitor = stock_monitor  # Queue or QueueObj
        self.time_scale = time_scale

    def on_epoch_end(self, epoch, logs=None):
        if self.repeat_predictions:
            preds = self.model.predict(self.trainX)
        else:
            preds = self.model.predict(self.testX)

        # Generate a figure with matplotlib
        if self.time_scale == '1s':
            figure = matplotlib.pyplot.figure(figsize=(20, 20))
            plot = figure.add_subplot(111)

            plot.plot(self.inverse_queue(self.trainY), color='blue')
            plot.plot(np.append(np.empty_like(self.trainY) * np.nan, self.inverse_queue(self.testY)), color='red')
            plot.plot(np.append(np.empty_like(self.trainY) * np.nan, self.inverse_queue(preds)), color='green')

            data = fig2data(figure)
            matplotlib.pyplot.close(figure)

            _1s_loss = 1.56

            wandb.log({f"1s-loss-{_1s_loss}": wandb.Image(data)}, commit=False)

        else:
            open = self.inverse_queue(self.trainX[0][0][0], mode='open')
            low = self.inverse_queue(self.trainX[0][0][1], mode='low')
            high = self.inverse_queue(self.trainX[0][0][2], mode='high')
            close = self.inverse_queue(self.trainX[0][0][3], mode='close')
            volume = self.inverse_queue(self.trainX[0][0][4], mode='volume')

            candle_stick = go.Candlestick(open=open,
                                          low=low,
                                          high=high,
                                          close=close)

            image = go.Figure(data=[candle_stick]).to_image()

            img = PILImage.frombytes('RGB', (20, 20), image)
            _1s_loss = 1.56
            # wandb.log({f"loss-{_1s_loss}-time scale:{self.time_scale}": wandb.Image(img)}, sync=False)

    def inverse_queue(self, arr, mode=None):
        if self.time_scale == '1s':  # Queue
            return arr * (self.stock_monitor._max - self.stock_monitor._min) + self.stock_monitor._min
        else:  # Candle
            return arr * (self.stock_monitor.candle[mode]._max - self.stock_monitor.candle[mode]._min) + \
                   self.stock_monitor.candle[mode]._min
