import wandb
from wandb.keras import WandbCallback
from libs.callback.plotutil import PlotCallback

class CallBack:
    def __init__(self):
        wandb.init()
        self.wandb=WandbCallback()
        self.neptun=None

    def plot_callback(self,model, trainX, trainY, testX, testY,stock_monitor,time_scale):
        return PlotCallback(model, trainX, trainY, testX, testY,stock_monitor,time_scale)

