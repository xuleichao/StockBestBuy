import os
import pandas as pd
import pickle
import pymysql
from sqlalchemy import create_engine

conn = create_engine('mysql+pymysql://root:111111@39.106.156.194:3306/my_gupiao?charset=utf8', pool_pre_ping=True)
con = conn.connect()

datasets = '../dataSets/stock_KL'

df = os.listdir(datasets)

df = [i for i in df if '.dataframe' in i] #获取所有的dataframe

new_df = pd.DataFrame([['']*14], columns=['date', 'begin_p', 'highest', 'lowest', 'end_p', 'amount', 'money', 'up_num', 'up_rate', 'smaller', 'high_low_diff', 'SH', 'SH_per', 's_name'])
for i in df:
    dt = open(datasets + '/' + i, 'rb').read()
    if len(dt) == 0:
        continue
    idf = pickle.loads(dt)
    idf = idf[: -1]
    idf['name'] = pd.DataFrame([i[: -10]] * idf.shape[0])
    idf.rename(columns={'日期': 'date', '开盘': 'begin_p', '最高': 'highest', '最低': 'lowest', '收盘': 'end_p', '成交量': 'amount', '成交金额': 'money', '升跌$': 'up_num', '升跌%': 'up_rate', '缩': 'smaller', '高低差%': 'high_low_diff', 'SH上证': 'SH', 'SH%': 'SH_per', 'name': 's_name'}, inplace = True)
    new_df = new_df.append(idf)
    break
new_df1 = new_df[1:]
new_df1['date'] = pd.to_datetime(new_df1['date'])
new_df1['begin_p'] = pd.to_numeric(new_df1['begin_p'])
new_df1['highest'] = pd.to_numeric(new_df1['highest'])
new_df1['lowest'] = pd.to_numeric(new_df1['lowest'])
new_df1['end_p'] = pd.to_numeric(new_df1['end_p'])

new_df1.to_sql('stock_KLine', con, if_exists='replace', index=False)
