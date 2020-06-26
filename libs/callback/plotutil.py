import matplotlib

matplotlib.use('Agg')  # noqa
import matplotlib.pyplot as plt
from tensorflow import keras
import numpy as np
import wandb
import apps.ai.config as config


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
        self.stock_name = 'APPL'
        self.figure_size = (20, 20)
        self.colors={'neg': {'pre':'black','gt':'pink','predict':'red'}, 'pos': {'pre':'gray','gt':'lightgreen','predict':'green'}}


    def format_decimal_points(self,number):
        return "{0:.2f}".format(number)

    def on_epoch_end(self, epoch, logs=None):
        # Generate a figure with matplotlib

        if self.time_scale == '1s':
            figure = matplotlib.pyplot.figure(figsize=self.figure_size)
            plot = figure.add_subplot(111)

            if config.prediction_type == config.MANY2ONE:
                plot.plot(self.inverse_queue(self.trainX[0][0]), color='blue')
                plot.plot(np.append(np.empty_like(self.trainX[0][0]) * np.nan, self.inverse_queue(self.trainY[0])),
                          color='blue')
                plot.plot(np.append(np.empty_like(np.append(self.trainX[0][0], self.trainY[0])) * np.nan,
                                    self.inverse_queue(self.testX[0][0])), color='blue')
                plot.plot(np.append(
                    np.empty_like(np.append(np.append(self.trainX[0][0], self.trainY[0]), self.testX[0][0])) * np.nan,
                    self.inverse_queue(self.testY[0])), color='red')
                plot.plot(np.append(
                    np.empty_like(np.append(np.append(self.trainX[0][0], self.trainY[0]), self.testX[0][0])) * np.nan,
                    self.inverse_queue(self.model.predict(self.testX))), color='green')

            data = fig2data(figure)
            matplotlib.pyplot.close(figure)

            wandb.log({f"{self.time_scale}/loss-{self.format_decimal_points(logs['loss'])}-val_loss-{self.format_decimal_points(logs['val_loss'])}": wandb.Image(data)}, commit=False, sync=True)

        else:
            if config.prediction_type == config.MANY2ONE:
                figure = self.get_candle_chart()
            else:
                pass

            data = fig2data(figure)
            matplotlib.pyplot.close(figure)

            _1s_loss = 1.56

            wandb.log({f"{self.time_scale}/loss-{self.format_decimal_points(logs['loss'])}-val_loss-{self.format_decimal_points(logs['val_loss'])}": wandb.Image(data)}, commit=False, sync=True)

    def inverse_queue(self, arr, mode=None):
        if self.time_scale == '1s':  # Queue
            return arr * (self.stock_monitor._max - self.stock_monitor._min) + self.stock_monitor._min
        else:  # Candle
            return arr * (self.stock_monitor.candle[mode]._max - self.stock_monitor.candle[mode]._min) + self.stock_monitor.candle[mode]._min

    def get_candle_chart(self):

        states = ['pre', 'GT', 'predict']
        stats=['low', 'open', 'close', 'high']   # todo: add volume
        fig, ax1 = plt.subplots(figsize=self.figure_size)
        ax1.set_title(f'{self.stock_name}')

        arr = np.array([])

        for i, val in enumerate(stats):
            if arr.size==0:
                arr=self.inverse_queue(
                    np.append(np.append(self.trainX[0][i][0], self.trainY[0][i*5:5*(i+1)]), self.testX[0][i][0]),
                    mode=val)
            else:
                arr=np.vstack((arr,self.inverse_queue(
                    np.append(np.append(self.trainX[0][i][0], self.trainY[0][i*5:5*(i+1)]), self.testX[0][i][0]),
                    mode=val)))

        pre_counter=i
        pre=arr

        arr = np.array([])
        for i,val in enumerate(stats):
            if arr.size==0:
                arr=self.inverse_queue(self.testY[0][i*5:5*(i+1)], mode=val)
            else:
                arr = np.vstack((arr, self.inverse_queue(self.testY[0][i*5:5*(i+1)], mode=val)))

        gt_counter = i
        gt=arr


        known_data = np.hstack((pre,gt))

        # rectangular box plot
        bplot1 = ax1.boxplot(known_data.T,
                             vert=True,  # vertical box alignment
                             patch_artist=True)   # fill with color

        self.add_candles(known_data,bplot1,pre_counter,gt_counter)


        #predict
        arr = np.array([])
        for i,val in enumerate(stats):
            if arr.size==0:
                arr = self.inverse_queue(self.model.predict(self.testX)[0][i*5:5*(i+1)],mode=val)
            else:
                arr=np.vstack((arr,self.inverse_queue(self.model.predict(self.testX)[0][i*5:5*(i+1)],mode=val)))

        arr=np.hstack((np.empty_like(pre)*np.nan,arr))

        self.add_candles(arr, bplot1, pre_counter, gt_counter)

        # adding horizontal grid lines
        for ax in [ax1]:
            ax.yaxis.grid(True)
        ax.set_xlabel('sample number')
        ax.set_ylabel('Price')


        return fig

    def color(self,state,i,pre_counter,gt_counter):
        if state:
            if i<pre_counter:
                return self.colors['pos']['pre']
            elif pre_counter<=i<pre_counter+gt_counter:
                return self.colors['pos']['gt']
            else:
                return self.colors['pos']['predict']
        else:
            if i<pre_counter:
                return self.colors['neg']['pre']
            elif pre_counter<=i<pre_counter+gt_counter:
                return self.colors['neg']['gt']
            else:
                return self.colors['neg']['predict']

    def add_candles(self,arr,bplot1,pre_counter,gt_counter):
        for i,(candle, patch) in enumerate(zip(arr, bplot1['boxes'])):
            open = candle[1]
            close = candle[2]
            if open <= close:
                patch.set_facecolor(self.color(True,i,pre_counter,gt_counter))
            else:
                patch.set_facecolor(self.color(False,i,pre_counter,gt_counter))