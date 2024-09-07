from pandas import Period
import backtrader
from Strategy.default_strategy import TestStrategyDefault
from datetime import datetime
import pandas
from Strategy.strategy_config import StrategyConfigBase
from Strategy.cfg.tdx_config import TdxStrategyConfigImpl
import math
from dateutil.relativedelta import relativedelta


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
        # self.ema_slow = backtrader.indicators.EMA(self.dataclose, period=self.params.slowPeriod)
        # self.ema_fast = backtrader.indicators.EMA(self.dataclose, period=self.params.fastPeriod)
        # self.dif = self.ema_fast - self.ema_slow
        # self.dea = backtrader.indicators.EMA(self.dif, period=self.params.difPeriod)
        
        # self.macd_history = backtrader.indicators.MACDHisto()
        self.macd = backtrader.indicators.MACD()

        self.cross = backtrader.indicators.CrossOver(
                self.macd.lines.macd, self.macd.lines.signal)

        self.value = 0
        self.max_value = self.value
        self.min_value = 0
        self.buy_value = 0
        self.win_cnt = 0
        self.lose_cnt = 0
        self.increase = 0
        self.decrease = 0
        self.busi_cnt = 0
        self.file_path = ''

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
                
                self.buy_value = self.broker.getvalue()
                self.busi_cnt += 1

            elif order.issell():

                # 同上

                self.log('MaStrategy sell execute Size:%d Price: %.2f, Cost: %.2f, Comm: %.2f' %
                         (order.executed.size,
                          order.executed.price,
                          order.executed.value,
                          order.executed.comm))
                
                if self.max_value < self.broker.getvalue():
                    self.max_value = self.broker.getvalue()
                    self.min_value = self.max_value
                elif self.min_value > self.broker.getvalue():
                    self.min_value = self.broker.getvalue()
                
                if self.buy_value < self.broker.getvalue():
                    self.increase += (self.broker.getvalue() - self.buy_value)
                    self.win_cnt += 1
                elif self.buy_value > self.broker.getvalue():
                    self.decrease += (self.buy_value - self.broker.getvalue())
                    self.lose_cnt += 1
                
                self.buy_value = 0

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

    def can_buy(self):
        return self.cross > 0

    def can_sell(self):
        return self.cross < 0

    def next(self):
        self.log('MaStrategy Close, %.2f' % self.dataclose[0])

        # 如果之前已经有订单在处理，但是还没处理完，就不再处理新订单 ( 这是当前策略处理的逻辑 )
        if self.order:
            return

        # 手里是否有头寸, 如果没有头寸就处理只处理买逻辑, 如果有头寸就处理卖逻辑
        dt = self.data.datetime.date(0).strftime("%Y-%m-%d")
        # print('date = %s', dt, self.dif[0], self.dea[0], self.ema_fast[0], self.ema_slow[0])
        if not self.position:
            if self.can_buy():
                max_price_size = self.get_max_size(self.dataclose[0])
                rise = (self.dataclose[0] -
                        self.dataclose[-1]) / self.dataclose[0]
                print(rise)
                if rise > 0.9:
                    price = self.dataclose[0] * (1 + 0.05)
                    max_price_size = math.floor(
                        self.broker.get_cash() / 100 / price) * 100
                print('%s : buy price: %.2f size: %d' %
                      (dt, self.dataclose[0], max_price_size))

                self.log('BUY CREATE , %.4f, %.1f' %
                         (self.dataclose[0], max_price_size))

                self.order = self.buy(size=max_price_size)
        else:
            if self.can_sell():
                print('%s : sell price: %.2f size: %d' %
                      (dt, self.dataclose[0], self.position.size))
                self.order = self.sell(size=self.position.size)

        # 获取当前的总价值
        self.value = self.broker.getvalue()

    def stop(self):
        dt2 = None
        dt2 = dt2 or self.datas[0].datetime.date(0)
        print('%s : End Portfolio Value: %.2f' %
              (dt2.isoformat(), self.value))
        
        if self.buy_value != 0:
            if self.max_value < self.broker.getvalue():
                self.max_value = self.broker.getvalue()
                self.min_value = self.max_value
            elif self.min_value > self.broker.getvalue():
                self.min_value = self.broker.getvalue()
                
            if self.buy_value < self.broker.getvalue():
                self.increase += (self.broker.getvalue() - self.buy_value)
                self.win_cnt += 1
            elif self.buy_value > self.broker.getvalue():
                self.decrease += (self.buy_value - self.broker.getvalue())
                self.lose_cnt += 1
            
        print('max rollback: %.2f%%\ntotal count: %d\nwin rate: %.2f%%\nearn rate: %.2f\n%.2f\n%.2f' % 
              ((self.max_value - self.min_value) * 100 / self.max_value,
               self.busi_cnt,
               self.win_cnt * 100 / (self.win_cnt + self.lose_cnt),
               self.increase / self.decrease,
               self.increase,
               self.decrease))

    def get_strategy_config() -> StrategyConfigBase:
        cfg = TdxStrategyConfigImpl()
        cfg.set_plot(True)
        cfg.set_data_path('E:/Workspace/code/backtrader/datas/tdx/sh600580.csv')
        cfg.set_start_date(datetime.now() - relativedelta(years=3))
        cfg.set_end_date(datetime.now())
        return cfg