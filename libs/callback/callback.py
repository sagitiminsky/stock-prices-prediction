import wandb
from wandb.keras import WandbCallback
from libs.callback.plotutil import PlotCallback

class CallBack:
    def __init__(self):
        wandb.init()
        self.wandb=WandbCallback()
        self.neptun=None

    def plot_callback(self,model, trainX, trainY, testX, testY,stock_monitor):
        return PlotCallback(model, trainX, trainY, testX, testY,stock_monitor)


# The init() function called this way assumes that
# NEPTUNE_API_TOKEN environment variable is defined.


# Define parameters
# PARAMS = {'decay_factor' : 0.5,
#           'n_iterations' : 117}

# Create experiment with defined parameters
# neptune.init('sagit/stocks_rnn')
# neptune.create_experiment (name='example_with_parameters',
#                           params=PARAMS)

