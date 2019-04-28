import numpy as np
from mpl_finance import candlestick_ohlc
from matplotlib.dates import DateFormatter, WeekdayLocator, DayLocator, MONDAY,date2num

#定义绘制K线图的函数
def pandas_candlestick_ohlc(stock_data, otherseries=None):
    # 设置绘图参数，主要是坐标轴
    mondays = WeekdayLocator(MONDAY)
    alldays = DayLocator()
    dayFormatter = DateFormatter('%d')
 
    fig, ax = plt.subplots()
    fig.subplots_adjust(bottom=0.2)
    if stock_data.index[-1] - stock_data.index[0] < pd.Timedelta('730 days'):
        weekFormatter = DateFormatter('%b %d')
        ax.xaxis.set_major_locator(mondays)
        ax.xaxis.set_minor_locator(alldays)
    else:
        weekFormatter = DateFormatter('%b %d, %Y')
    ax.xaxis.set_major_formatter(weekFormatter)
    ax.grid(True)
 
    # 创建K线图
    stock_array = np.array(stock_data.reset_index()[['date','open','high','low','close']])
    stock_array[:,0] = date2num(stock_array[:,0])
    candlestick_ohlc(ax, stock_array, colorup = "red", colordown="green", width=0.6)
 
    # 可同时绘制其他折线图
    if otherseries is not None:
        for each in otherseries:
            plt.plot(stock_data[each], label=each)
        plt.legend()
 
    ax.xaxis_date()
    ax.autoscale_view()
    plt.setp(plt.gca().get_xticklabels(), rotation=45, horizontalalignment='right')
    plt.show()

from pandas import read_excel
import pickle
## 读取excel文件，并将‘日期’列解析为日期时间格式,并设为索引
stock_data=read_excel('../abc.xlsx',parse_dates=['日期'],index_col='日期')
stock_data.index.name='日期' #日期为索引列
#将数据按日期这一列排序（保证后续计算收益率的正确性）

stock_data.index.name='date' #日期为索引列
#对股票数据的列名重新命名
stock_data.columns=['open','high','low','close','volume','market_value','turnover','pe','pb']
data=stock_data.loc['2016-02-15':'2016-03-31']  #获取某个时间段内的时间序列数据
pandas_candlestick_ohlc(data)

