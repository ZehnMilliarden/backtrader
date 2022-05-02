
# https://blog.csdn.net/h00cker/category_11448348.html

from __future__ import (absolute_import, division, print_function, unicode_literals)
from datetime import datetime

import runtime
runtime.CurrentWorkPathInstance.AddCurrentWorkPath()

import pandas as pd
import backtrader as bt

class TestStrategy(bt.Strategy):

    def log(self, txt, dt=None):
        ''' 提供记录功能 '''
        dt = dt or self.datas[0].datetime.date(0)
        print('%s, %s' % (dt.isoformat(), txt))

    def __init__(self):
        # 引用到 输入数据的close价格
        self.dataclose = self.datas[0].close

    def next(self):
        self.log('Close, %.2f' % self.dataclose[0])

if __name__ == '__main__':

    cerebro = bt.Cerebro()

    cerebro.addstrategy(TestStrategy)

    stock_data_raw = pd.read_csv('datas\yhoo-2014.txt', index_col='Date', parse_dates=True)
    # print(stock_data_raw)

    start_date = datetime(2014,1,2)
    end_date = datetime(2014,12,31)

    stock_data = bt.feeds.PandasData(dataname=stock_data_raw, fromdate=start_date,todate=end_date)

    cerebro.adddata(stock_data)

    cerebro.broker.setcash(100000.0)

    print('Starting Portfolio Value: %.2f' % cerebro.broker.getvalue())
    cerebro.run()
    print('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())