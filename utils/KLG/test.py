import tushare as ts
import matplotlib.pyplot as plt
import numpy as np
import mpl_finance as mpf
import matplotlib.ticker as ticker
import tushare as ts
import matplotlib.pyplot as plt
import numpy as np
data = ts.get_k_data('002400', ktype='D', autype='qfq', start='2017-09-17', end='')
prices = data[['open', 'high', 'low', 'close']][:30]
dates = data['date'][:30]
candleData = np.column_stack([list(range(len(dates))), prices])
fig = plt.figure(figsize=(10, 6))
ax = fig.add_axes([0.1, 0.3, 0.8, 0.6])
ax.xaxis.set_major_locator(ticker.MultipleLocator(1))
#ax.set_xticklabels(dates, rotation=90)
ax.grid(True, linestyle='-.')
mpf.candlestick_ohlc(ax, candleData, width=0.5, colorup='r', colordown='b')

plt.savefig('test.jpg')
#plt.show()
