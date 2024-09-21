from pandas import Period
import backtrader
from Strategy.default_strategy import TestStrategyDefault
from datetime import datetime
import pandas
from Strategy.strategy_config import StrategyConfigBase
from Strategy.cfg.tdx_config import TdxStrategyConfigImpl
import math
from dateutil.relativedelta import relativedelta
import numpy
import sys


class MacdStrategy(TestStrategyDefault):
    params = {
        "exit_bar": 5,
        "fastPeriod":12,
        "slowPeriod":26,
        "difPeriod":9
    }

    def __init__(self):
        super(MacdStrategy, self).__init__()

        self.order = None
        self.macd = backtrader.indicators.MACDHisto()

        self.cross = backtrader.indicators.CrossOver(
                self.macd.lines.macd, self.macd.lines.signal)
        
        self.cache_length = 5
        self.twist_threshold = 0.2
        self.big_rise_threshold = 0.5

        self.near_by = []
        self.near_len = 5

        self.near_far = []
        self.far_len = 9

        self.last_price = 0

        #sys.stdout = open('macd_var.txt', 'w')

    def notify_order(self, order):

        if self.order is None:
            return

        if order.status in [order.Submitted, order.Accepted]:
            # 订单状态处于，提交订单, 订单被接受
            return

        if order.status in [order.Completed]:

            order.executed.log()

            if order.isbuy():

                # order.executed.price 订单单价
                # order.executed.value 订单价值
                # order.executed.comm  订单佣金

                self.log('MaStrategy buy execute Size:%d Price: %.2f, Cost: %.2f, Comm: %.2f' %
                         (order.executed.size,
                          order.executed.price,
                          order.executed.value,
                          order.executed.comm
                          ))
                
                self.last_price = order.executed.price

            elif order.issell():

                # 同上

                self.log('MaStrategy sell execute Size:%d Price: %.2f, Cost: %.2f, Comm: %.2f' %
                         (order.executed.size,
                          order.executed.price,
                          order.executed.value,
                          order.executed.comm))

            else:
                self.log('MaStrategy unrecorgnized order: %s' %
                         order.status)

            # 执行完毕的订单 bar 的位置, 不区分购买还是出售订单
            self.bar_executed = len(self)

        elif order.status in [order.Canceled]:
            # 订单 用户取消, 保证金
            self.log('Order %s', order.Canceled.__str__)

        elif order.status in [order.Rejected]:
            # 订单 经纪人拒绝订单
            self.log('Order %s', order.Rejected.__str__)

        elif order.status in [order.Margin]:
            # 订单 保证金不足（现金不足）如果次日股票高开高走，价格都超过本日收盘价，你的现金就买不起这么多的股票，出现Margin状态
            dt = self.data.datetime.date(0).strftime("%Y-%m-%d")
            self.log('Order %s', order.Margin.__str__)

        self.order = None
    
    def check_has_cross(self):
        if(self.cross > 0):
            return True
    
        crossed = False
        for i in range(0 - self.cache_length, -1):
            if self.macd.lines.histo[i - 1] < 0 and self.macd.lines.histo[i] > 0 :
                crossed = True
                break

        return crossed

    def check_rise_single(self, arr, inc):
        for i in range(1, len(arr)):
            if inc and arr[i] < arr[i - 1]:
                return False
            elif (not inc) and arr[i] > arr[i - 1]:
                return False
        return True

    def check_is_twisted(self, inc):
        subArr = []
        for i in range(0 - self.cache_length, 0):
            subArr.append(self.macd.lines.histo[i - 1])
        return self.check_rise_single(subArr, inc)
    
    def is_sub_increasing(self):
        subArr = []
        for i in range(0 - self.cache_length, 0):
            subArr.append(self.macd.lines.histo[i] - self.macd.lines.histo[i - 1])
        
        return self.check_rise_single(subArr, True)
    
    def is_big_rise(self):
        return self.macd.lines.macd[0] - self.macd.lines.macd[-1] > self.big_rise_threshold
    
    def is_decrease_treshold(self):
        return self.last_price > 0 and (self.dataclose[0] / self.last_price) <= 0.93

    def can_buy(self):
        return self.is_sub_increasing() and self.macd.lines.histo[0] > 0
        return self.cross > 0
        if self.is_big_rise():
            return True
        elif self.check_is_twisted():
            return False
        else:
            return self.macd.histo[0] > self.macd.histo[-1]

    def can_sell(self):
        if self.is_decrease_treshold():
            return True;
        #return self.check_is_twisted(False)
        return self.cross < 0 #or self.check_is_twisted()
        return self.macd.histo[0] < self.macd.histo[-1]

    def next(self):
        self.log('MaStrategy Close, %.2f' % self.dataclose[0])

        if len(self.near_by) >= self.near_len:
            self.near_by.pop(0)
        self.near_by.append(self.macd.lines.histo[0])
        
        if len(self.near_far) >= self.far_len:
            self.near_far.pop(0)
        self.near_far.append(self.macd.lines.histo[0])

        # 如果之前已经有订单在处理，但是还没处理完，就不再处理新订单 ( 这是当前策略处理的逻辑 )
        if self.order:
            return

        # 手里是否有头寸, 如果没有头寸就处理只处理买逻辑, 如果有头寸就处理卖逻辑
        dt = self.data.datetime.date(0).strftime("%Y-%m-%d")
        #print(dt, numpy.var(self.near_by), numpy.std(self.near_by))
        #print(dt, numpy.var(self.near_far), numpy.std(self.near_far))
        if not self.position:
            if self.can_buy():
                max_price_size = math.floor(
                        self.broker.get_cash() * 0.95 / 100 / self.dataclose[0]) * 100

                self.log('BUY CREATE , %.4f, %.1f' %
                         (self.dataclose[0], max_price_size))

                self.order = self.buy(size=max_price_size)
        else:
            if self.can_sell():
                self.order = self.sell(size=self.position.size)

        # 获取当前的总价值
        self.value = self.broker.getvalue()

    def stop(self):
        dt2 = None
        dt2 = dt2 or self.datas[0].datetime.date(0)
        #sys.stdout = sys.__stdout__

    def get_strategy_config() -> StrategyConfigBase:
        cfg = TdxStrategyConfigImpl()
        cfg.set_plot(True)
        cfg.set_data_path('D:/Workspace/backtrader/datas/tdx/sh603298.csv')
        cfg.set_start_date(datetime.now() - relativedelta(years=3))
        cfg.set_end_date(datetime.now())
        return cfg