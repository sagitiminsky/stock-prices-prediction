import matplotlib

# matplotlib.use('Agg')  # noqa
import matplotlib.pyplot as plt


import numpy as np


def plt_4_candle_chart(stock_name, arr,figure_size):
    # Random test data
    all_data = arr.T
    labels = range(len(arr.T[0]))

    fig, ax1 = plt.subplots(figsize=figure_size)

    # rectangular box plot
    bplot1 = ax1.boxplot(all_data,
                         vert=True,  # vertical box alignment
                         patch_artist=True,  # fill with color
                         labels=labels)  # will be used to label x-ticks
    ax1.set_title(f'{stock_name}')

    # fill with colors
    colors = {'neg':'pink', 'pos':'lightgreen'}

    for candle,patch in zip(arr,bplot1['boxes']):
        open=candle[1]
        close=candle[2]
        if open<=close:
            patch.set_facecolor(colors['pos'])
        else:
            patch.set_facecolor(colors['neg'])

    # adding horizontal grid lines
    for ax in [ax1]:
        ax.yaxis.grid(True)
        ax.set_xlabel('sample number')
        ax.set_ylabel('Price')

    # fig.show()

    return fig


if '__main__' == __name__:
    plt_4_candle_chart('APPL', np.array([np.array([1, 2,3, 4]), np.array([5, 7,6, 8])]))
