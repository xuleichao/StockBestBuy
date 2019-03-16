import re
import urllib.request
from pandas import DataFrame
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
    # 如果监测到文本中包含股票代码
    if code:
        # 获取股票的名称
        name = text\
            .replace('(', "")\
            .replace(')', "")\
            .replace(code[0], '')
        return name, code[0]

if __name__ == '__main__':
    url = 'http://quote.eastmoney.com/stocklist.html'
    soup = get_soup(url)
    lis = soup.find_all('li')
    rslt = []
    for i in lis:
        if li_filter(i):
            a = regex_get_stock_code(i.text)#从抓取的文本中获取股票代码信息
            if a:
                rslt.append(a)
    # 数据转换为dataframe表格
    stock_df = DataFrame(rslt, columns=['name', 'code'])
    # 将数据写入文件
    with open('./dataSets/stock_codes.txt', 'w', encoding='utf-8') as f:
        for i in rslt:
            f.write('\t'.join(i)+'\n')


