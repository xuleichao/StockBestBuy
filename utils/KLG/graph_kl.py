import tushare as ts
import matplotlib.pyplot as plt
import numpy as np
import mpl_finance as mpf
import matplotlib.ticker as ticker
from utils.tagging_data_util import get_data_main
from utils.dataframe_2_sql import df_in_db
import tushare as ts
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import datetime
import pickle

def labels_util(dates, data):
    dates_lst = dates.values.tolist()
    dates_lst.reverse()
    data_x = [str(int(i[0])) for i in data]
    rslt = list(zip(dates_lst, data_x))
    return rslt

def gnrt_end_date(start, gap=30):
    # 生成一个间隔的时间start = 2017-09-17 间隔30天 end=2017-10-17
    start_time = datetime.datetime.strptime(start,'%Y-%m-%d')
    end_time = start_time + datetime.timedelta(days=gap)
    end_time_str = end_time.strftime('%Y-%m-%d')
    return end_time, end_time_str

def get_stock_data(code, start):
    end = gnrt_end_date(start)
    data = ts.get_k_data(code, ktype='D', autype='qfq', start=start, end=end)
    print(data.shape)
    if data.shape[0] != 0:
        return data

def get_stock_data2(df, start):
    endtime, endtime_str = gnrt_end_date(start)
    df_for_tag = df[(df['date_time'] > start) & (df['date_time'] < endtime)]
    if df_for_tag.shape[0] != 0:
        return df_for_tag
    else:
        # todo 整个一个月都没数据，那就从endtime开始进行数据提取
        new_start = datetime.datetime.strftime(endtime, '%Y-%m-%d')
        new_endtime, new_endtime_str = gnrt_end_date('2013-11-21')
        df_for_tag = df[(df['date_time'] > new_start) & (df['date_time'] < new_endtime)]
        if df_for_tag.shape[0] != 0:
            return df_for_tag
        return None


def graph_main_old(tag_df, start='2017-09-01', code=None):
    data = get_stock_data2(tag_df, start)
    # 将数据导入数据库
    #df_in_db(data, code)
    with open('./dataSets/data.temp', 'wb') as f:
        f.write(pickle.dumps([data, code]))
    prices = data[['open', 'high', 'low', 'close']]
    prices_lst = prices.values.tolist()
    prices_lst.reverse()
    prices = pd.DataFrame(prices_lst, columns=['open', 'high', 'low', 'close'])
    dates = data['date_time'].apply(lambda x: datetime.datetime.strftime(x,"%Y-%m-%d"))
    candleData = np.column_stack([list(range(len(dates))), prices])
    fig = plt.figure(figsize=(10, 6))
    ax = fig.add_axes([0.1, 0.3, 0.8, 0.6])
    ax.xaxis.set_major_locator(ticker.MultipleLocator(1))
    #ax.set_xticklabels(dates, rotation=45)
    ax.grid(True, linestyle='-.')
    mpf.candlestick_ohlc(ax, candleData, width=0.5, colorup='r', colordown='b')

    plt.savefig('./static/images/test.png')
    #plt.show()
    return labels_util(dates, candleData), code

def graph_main():
    tag_df, begin_time, code = get_data_main()
    result = graph_main_old(tag_df, start=begin_time, code=code)
    return result

if __name__ == '__main__':
    z = graph_main()
