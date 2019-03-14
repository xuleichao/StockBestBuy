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

if __name__ == '__main__':
    url = 'http://quote.eastmoney.com/stocklist.html'
    soup = get_soup(url)
    lis = soup.find_all('li')
    for i in lis:
        if li_filter(i):
            print(i.text)

