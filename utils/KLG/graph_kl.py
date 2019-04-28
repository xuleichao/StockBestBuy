import tushare as ts
import matplotlib.pyplot as plt
import numpy as np
import mpl_finance as mpf
import matplotlib.ticker as ticker
import tushare as ts
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

def labels_util(dates, data):
    dates_lst = dates.values.tolist()
    data_x = [str(int(i[0])) for i in data]
    rslt = list(zip(dates_lst, data_x))
    return rslt

def graph_main(code='002400', start='2017-09-17', end='2017-09-22'):
    data = ts.get_k_data(code, ktype='D', autype='qfq', start=start, end=end)
    prices = data[['open', 'high', 'low', 'close']]
    dates = data['date']
    candleData = np.column_stack([list(range(len(dates))), prices])
    fig = plt.figure(figsize=(10, 6))
    ax = fig.add_axes([0.1, 0.3, 0.8, 0.6])
    ax.xaxis.set_major_locator(ticker.MultipleLocator(1))
    #ax.set_xticklabels(dates, rotation=45)
    ax.grid(True, linestyle='-.')
    mpf.candlestick_ohlc(ax, candleData, width=0.5, colorup='r', colordown='b')

    plt.savefig('./static/images/test.png')
    #plt.show()
    return labels_util(dates, candleData)


if __name__ == '__main__':
    z = graph_main()
