import re
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
    pass

if __name__ == '__main__':
    for i in stock_codes_data:
        get_KLine_data(i[1])
