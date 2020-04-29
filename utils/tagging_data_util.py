'''主要是为了获得标注数据，从数据中获取未标注的数据，给前台'''
import pandas as pd
import pickle
import os
import datetime
from utils.dataframe_2_sql import get_data_from_tagging_table
from utils.dataframe_2_sql import get_in_tagging_stock
from utils.dataframe_2_sql import random_a_stock
main_path = os.path.dirname(os.path.abspath(__file__)).replace('\\', '/')
main_path = '/'.join(main_path.split('/')[:-2])

base_path = main_path + '/StockBestBuy/dataSets/stock_KL'

def get_dataframe(name):
    df = pickle.load(open(base_path + '/' + name+'.dataframe', 'rb'))
    df = df[: -1]# 最后一行没用
    useful_header = ['日期', '开盘', '最高', '最低', '收盘']
    df = df[useful_header]
    df['date_time'] = pd.to_datetime(df['日期'])
    df['open'] = pd.to_numeric(df['开盘'])
    df['high'] = pd.to_numeric(df['最高'])
    df['low'] = pd.to_numeric(df['最低'])
    df['close'] = pd.to_numeric(df['收盘'])
    for i in useful_header:
        df.pop(i)
    last_time = df.head(1)['date_time'] #获取最近的时间

    return df, last_time

def get_data_main():
    get_tag_info = get_in_tagging_stock() # 获取正在标注的股票
    if get_tag_info[0] == True:
        code = get_tag_info[1][1]  # 股票代码
        name = get_tag_info[1][0]  # 上市公司名称
        if name[0] == '*':
            name = name.replace('*', '_')
        tagging_stock_info = get_data_from_tagging_table(code) #从标注表中获取股票信息。返回最后的日期
        if tagging_stock_info:
            # 获取本地股票的dataframe，第一项是dataframe，第二项是最近日期
            local_df, local_last_time = get_dataframe(name)
            local_last_time = datetime.datetime.fromtimestamp(datetime.datetime.timestamp(local_last_time[0]))
            if tagging_stock_info >= local_last_time:
                print('已经标注完毕')
                # 开始进行新的标注，在未标注的股票中随机生成一直股票进行标注
                random_a_stock()
                recurse_rslt = get_data_main()
                return recurse_rslt
            else:
                # 开始最新日期后一天开始标注
                tagging_stock_info_str = datetime.datetime.strftime(tagging_stock_info,'%Y-%m-%d')
                return local_df, tagging_stock_info_str, code
        else:
            #说明没有获取到标注信息，可以从头开始标注
            # 获取本地股票的dataframe，第一项是dataframe，第二项是最近日期
            local_df, local_last_time = get_dataframe(name)
            begin_time = local_df.tail(1)['date_time'] #获取最早的时间
            return local_df, begin_time.apply(lambda x: datetime.datetime.strftime(x,"%Y-%m-%d")).values.tolist()[0], code


    else:
        # 说明没有获取到任何已经开始标注的股票，可以随机生成一只股票进行标注
        random_a_stock()
        recurse_rslt = get_data_main()
        return recurse_rslt


if __name__ == '__main__':
    name = '50等权'
    get_dataframe(name)
