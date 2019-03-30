import re
import pickle
import urllib.request
from pandas import DataFrame
from bs4 import BeautifulSoup as bsp
from StockCodeAquire import get_soup

# 读取股票与代码数据
data_path = './dataSets/stock_codes.txt'
f = open(data_path, 'r', encoding='utf-8')
stock_codes_data = f.readlines()
f.close()
stock_codes_data = [i.strip().split('\t') for i in stock_codes_data]

base_url = 'http://www.aigaogao.com/tools/history.html?s='

def get_KLine_data(code):
    '''传入股票代码，获得K线'''
    soup = get_soup(base_url + code)
    data = get_table_data(soup)
    data_df = DataFrame(data[1: ], columns=data[0])
    return data_df

def get_table_data(soup):
    '''获得网页中的table数据'''
    tables = soup.find_all('table')
    table = tables[-1] # 股价数据table
    trs = table.find_all('tr') # 每个tr 是一行，找出table中的所有tr
    result = []
    for i in trs:
        tds = i.find_all('td')
        sub_rslt = []
        for j in tds:
            sub_rslt.append(j.text)
        result.append(sub_rslt)
    return result

if __name__ == '__main__':
    for i in stock_codes_data:
        try:
            z = get_KLine_data(i[1])
        except:
            pass
        with open('./dataSets/stock_KL/%s.dataframe'%i[0].strip(), 'wb') as f:
            f.write(pickle.dumps(z))

