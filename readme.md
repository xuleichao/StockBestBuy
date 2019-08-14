## 介绍
- 通过分析股票的价格走势，K线特征来判断股票是不是最佳的买入时间

---
## 步骤
1. 爬取历史股价，K线(完成)
- [所有股票代码](http://quote.eastmoney.com/stocklist.html)(完成)
- [股票数据](http://www.aigaogao.com/tools/history.html)(完成)
- 数据标注(正在进行)
2. 建模
![蜡烛图](https://github.com/xuleichao/StockBestBuy/blob/master/static/images/%E8%9C%A1%E7%83%9B%E5%9B%BE.jpg)
- 建模步骤：根据蜡烛图建模，获得各个组件所占比例。需要获得如下比例

    1. 蜡烛图总长度为基准
    2. 上影线所占基准的比例(百分比，不保留小数)
    3. 下影线所占基准的比例(百分比，不保留小数)
    4. 实体所占基准的比例(百分比，不保留小数)
- 函数参数
    1. 参数---func(最高价，收盘价，开盘价，最低价)
    2. 基准长度 = 最高价 - 最低价
    3. 上影线长度 = 最高价 - 收盘价
    4. 下影线长度 = 开盘价 - 最低价
    5. 实体长度 = 收盘价 - 开盘价
    6. 返回 上影线比例， 下影响比例，实体比例
3. 预测

附：
[BeautifulSoup文档](https://www.crummy.com/software/BeautifulSoup/bs4/doc/index.zh.html)
