import re
import pandas as pd
import numpy as np
import urllib.request

from bs4 import BeautifulSoup as bsp

def get_soup(url):
    """获得指定url 的HTML，并返回soup"""
    html_data = urllib.request.urlopen(url).read()
    soup = bsp(html_data, 'lxml')
    return soup

def li_filter(li):
    if '(' in li.text:
        return li

def regex_get_stock_code(text):
    '''传入股票和股票代码-京东(00001)'''
    reg = '\(([0-9]+)\)'
    code = re.findall(reg, text)
    return code

if __name__ == '__main__':
    url = 'http://quote.eastmoney.com/stocklist.html'
    soup = get_soup(url)
    lis = soup.find_all('li')
    count = 0
    for i in lis:
        if li_filter(i):
            print(i.text)
            a = regex_get_stock_code(i.text)
            print(a)
            count += 1
    print(count)

