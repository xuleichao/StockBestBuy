import requests
from bs4 import BeautifulSoup as bsp
import pandas as pd
from pandas import DataFrame
import numpy as np
import time

def time_to_timestr(time_data):
    if type(time_data) == type('sss'):
        return time_data
    # 将时间数据格式转换为时间字符串
    # time_data.timestamp() 变成时间戳
    timestruct = time.localtime(time_data.timestamp())
    time_str = time.strftime('%Y-%m-%d', timestruct)
    return time_str

def gujianew(code, riqi):
    url = 'http://www.aigaogao.com/tools/history.html?s=' + code
    detail_url = requests.get(url)
    soup = bsp(detail_url.content, 'lxml')
    detail_content = soup.find_all('table')
    #print(detail_content)
    table = detail_content[-1]
    #print(table)
    trs = table.find_all('tr')
    # print(trs)
    trs_list = []
    for i in trs:
        # print(i)
        tds = i.find_all('td')
        # print(tds)
        tr_list = []
        for j in tds:
            tr_list.append(j.text)
        trs_list.append(tr_list)
    #print(trs_list[0])
    result = DataFrame(trs_list[1:-1], columns=trs_list[0])
    #print(result)
    result['日期'] = pd.to_datetime(result['日期'])
    #print(riqi)
    #print(result['日期'])
    finally_result = result[result['日期']>riqi]
    #finally_result = [[time_to_timestr(j) for j in i] for i in finally_result.values]
    print(finally_result, type(finally_result))
    a = finally_result
    print(s)
    fw = open('./002401.txt', 'a', encoding='utf-8')
    for l in s[0]:
        fw.write(str(l)+'\t')
    
    #a = finally_result.values.to_list()
    #a = np.array(finally_result).to_list()
    #print(a)






if __name__ == '__main__':
    file = open('./002400.txt', 'r', encoding='utf-8').readlines()
    #print(file)
    head = file[0]
    #print(type(head)) #是字符串
    head = file[0].strip().split('\t')
    #print(head)
    data = file[1:-1]
    #print(type(data)) #是列表
    data_list = []
    for i in data:
        i = i.strip().split('\t')
        data_list.append(i)
    #print(data_list)
    data_df = DataFrame(data_list, columns=head)
    #print(data_df)
    data_df['日期'] = pd.to_datetime(data_df['日期'])
    data_df = data_df['日期'].sort_index()
    #print(data_df)
    #print(data_df['日期'])
    #print(type(data_df))
    riqi = data_df.iloc[0]
    #print(riqi)
    gujianew('002400', riqi)

