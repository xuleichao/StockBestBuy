import os
import random
import pandas as pd
import pickle
import pymysql
import time
from sqlalchemy import create_engine
from config.db_config import db_config

def get_db_sys():
    conn = create_engine('mysql+pymysql://%s:%s@%s:%s/stock_best_buy?charset=utf8'%(db_config['user_name'],
                                                                         db_config['password'],
                                                                        db_config['IP'],
                                                                        db_config['port']),
                         pool_pre_ping=True)
    con = conn.connect()
    return conn, con

def get_in_tagging_stock():
    # 获取正在标注的股票
    sql = 'select * from stocks_tagging_state where tag_state=\'1\';'
    db_info = get_db_sys()
    info = db_info[1].execute(sql)
    data = info.fetchone()
    if data:
        return True, data
    else:
        return False, None

def get_data_from_tagging_table(code):
    # 从标注数据表中获取正在标注股票的最近日期，并与本地数据做比较
    sql = 'select * from stock_tagging_data where stock_code=\'%s\' order by date_time desc'%code
    db_info = get_db_sys()
    info = db_info[1].execute(sql)
    data = info.fetchone()
    if data:
        last_time = data[0]
        return last_time
    else:
        return None

def random_a_stock(stock_list=None):
    # 随机生成一只用于标注的股票 stock_list 为随机列表，默认不传入
    sql = 'select * from stocks_tagging_state where tag_state=\'0\';'
    db_info = get_db_sys()
    info = db_info[1].execute(sql)
    data = info.fetchall()
    if len(data) == 0:
        print('都已经标注完了')
        return None
    rand_num = random.randint(0, len(data)) # 随机生成一只股票啦
    stock_code = data[rand_num][1] # 股票代码
    update_sql = 'update stock_tagging_state set tag_state=\'1\' where code=\'%s\''%stock_code
    db_info[1].execute(update_sql)

def df_in_db(df, code):
    # 将dataframe导入数据库
    df['stock_code'] = code
    df['tagging'] = '0'
    conn, con = get_db_sys()
    df.to_sql('stock_tagging_data', con, if_exists='append', index=False)

def update_db_data(tag_dict):
    # 将标注结果更新到数据库中
    _, con = get_db_sys()
    update_sql = '''update stock_tagging_data set tagging=\'1\' 
    where date_format(date_time, '%s')=\'%s\' and stock_code=\'%s\''''
    for i,j in tag_dict:
        date_time, code = j.split(',') # 获取时间与股票代码
        con.execute(update_sql%('%%Y-%%m-%%d', date_time, code))


if __name__ == '__main__':
    a = get_data_from_tagging_table('n')
    datasets = '../dataSets/stock_KL'
    df = os.listdir(datasets)
    df = [i for i in df if '.dataframe' in i] #获取所有的dataframe
    codes = ''
    new_df1.to_sql('stock_KLine', con, if_exists='replace', index=False)
