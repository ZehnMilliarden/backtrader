
# https://blog.csdn.net/h00cker/category_11448348.html

from __future__ import (absolute_import, division, print_function, unicode_literals)
from datetime import datetime

import runtime
runtime.CurrentWorkPathInstance.AddCurrentWorkPath()

import pandas as pd
import backtrader as bt

class TestStrategyDefault(bt.Strategy):

    def log(self, txt, dt=None):
        ''' 提供记录功能 '''
        dt = dt or self.datas[0].datetime.date(0)
        print('%s, %s' % (dt.isoformat(), txt))

    def __init__(self):
        # 引用到 输入数据的close价格
        self.log('TestStrategyDefault __init__')
        self.dataclose = self.datas[0].close

    def next(self):
        self.log('TestStrategyDefault Close, %.2f' % self.dataclose[0])

class TestStrategyPlanA(TestStrategyDefault):

    def __init__(self):
        # 引用到 输入数据的close价格
        TestStrategyDefault.__init__(self)

    def next(self):
        self.log('TestStrategyPlanA Close, %.2f' % self.dataclose[0])
        if self.dataclose[0] < self.dataclose[-1] and self.dataclose[-1] < self.dataclose[-2]:
            # 连续下跌两天就买入
            self.log('TestStrategyPlanA buy create %.2f' % self.dataclose[0])
            self.buy()

class TestStrategyPlanB(TestStrategyDefault):

    def __init__(self):
        # 引用到 输入数据的close价格
        TestStrategyDefault.__init__(self)
        self.order = None

    def notify_order(self, order):
        if order.status in [order.Submitted, order.Accepted]:
            return
        
        if order.status in [order.Completed]:
            if order.isbuy():
                self.log('TestStrategyPlanB buy execute: %.2f' % order.executed.price)
            else:
                self.log('TestStrategyPlanB sell execute: %.2f' % order.executed.price)

            self.bar_executed = len(self)
        elif order.status in [order.Canceled, order.Margin, order.Rejected]:
           self.log('Order Canceled/Margin/Rejected')
        
        self.order=None

    def next(self):
        self.log('TestStrategyPlanB Close, %.2f' % self.dataclose[0])

        if self.order:
            return

        if not self.position:

            if self.dataclose[0] < self.dataclose[-1] and self.dataclose[-1] < self.dataclose[-2]:
                # 连续下跌两天就买入
                self.log('TestStrategyPlanB buy create %.2f' % self.dataclose[0])
                self.buy()
        else:
            
            if len(self) >= self.bar_executed+5:
                self.log('TestStrategyPlanB sell create %.2f' % self.dataclose[0])
                self.order = self.sell()

class TestStrategyManager:

    def __init__(self):
        self.__StrategyType = 0

    def SetStrategy(self, StrategyType):
        self.__StrategyType=StrategyType

    def GetStrategy(self):
        if self.__StrategyType == 0:
            return TestStrategyDefault
        elif self.__StrategyType == 1:
            return TestStrategyPlanA
        elif self.__StrategyType == 2:
            return TestStrategyPlanB
        return TestStrategyDefault

if __name__ == '__main__':

    cerebro = bt.Cerebro()

    strategyManager = TestStrategyManager()
    strategyManager.SetStrategy(2)

    cerebro.addstrategy(strategyManager.GetStrategy())

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