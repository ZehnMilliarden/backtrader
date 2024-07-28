
from pandas import Period
import backtrader
from Strategy.default_strategy import TestStrategyDefault
from datetime import datetime
import pandas
from Strategy.strategy_config import StrategyConfigBase
from Strategy.cfg.tdx_config import TdxStrategyConfigImpl
import math
from dateutil.relativedelta import relativedelta
import enum

MaStrategyEnum = enum.Enum('MaStrategyEnum', ('SMA', 'MMA', 'EMA', 'MEMA'))

class MaStrategy(TestStrategyDefault):

    # 外部传参
    params = {
        "exit_bar": 5,
        "maperiod": 20,
        "sma_slow": 20,
        "sma_fast": 10,
        "ema_day": 20,
        "ema_slow": 50,
        "ema_fast": 10,
        "ma_strategy_enum": MaStrategyEnum.MMA
    }

    def __init__(self):
        # order 用于标记 当前正在处理的订单\
        super(MaStrategy, self).__init__()

        self.order = None

        if self.params.ma_strategy_enum == MaStrategyEnum.SMA:
            self.sma = backtrader.indicators.SMA(
                self.dataclose, period=self.params.maperiod)
        elif self.params.ma_strategy_enum == MaStrategyEnum.MMA:
            self.sma_fast = backtrader.indicators.SMA(period=self.params.sma_fast)
            self.sma_slow = backtrader.indicators.SMA(period=self.params.sma_slow)
            self.sma_cross = backtrader.indicators.CrossOver(self.sma_fast, self.sma_slow)
        elif self.params.ma_strategy_enum == MaStrategyEnum.EMA:
            self.ema = backtrader.indicators.EMA(self.dataclose, period=self.params.ema_day)
        else:
            self.ema_fast = backtrader.indicators.SMA(period=self.params.ema_fast)
            self.ema_slow = backtrader.indicators.SMA(period=self.params.ema_slow)
            self.ema_cross = backtrader.indicators.CrossOver(self.ema_fast, self.ema_slow)

        # 记录当前的价值
        self.value = 0

    # 订单状态变更
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

                self.log('MaStrategy buy execute Size:%d Price: %.2f, Cost: %.2f, Comm: %.2f, period: %d' %
                         (order.executed.size,
                          order.executed.price,
                          order.executed.value,
                          order.executed.comm,
                          self.params.maperiod))

            elif order.issell():

                # 同上

                self.log('MaStrategy sell execute Size:%d Price: %.2f, Cost: %.2f, Comm: %.2f, period: %d' %
                         (order.executed.size,
                          order.executed.price,
                          order.executed.value,
                          order.executed.comm,
                          self.params.maperiod))

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
        if self.params.ma_strategy_enum == MaStrategyEnum.SMA:
            return (self.dataclose[0] > self.sma[0]) and (self.dataclose[-1] <= self.sma[-1])
        elif self.params.ma_strategy_enum == MaStrategyEnum.MMA:
            return self.sma_cross > 0
        elif self.params.ma_strategy_enum == MaStrategyEnum.EMA:
            return self.dataclose[0] > self.ema[0]
        else:
            return self.ema_cross > 0
        
    def can_sell(self):
        if self.params.ma_strategy_enum == MaStrategyEnum.SMA:
            return self.dataclose[0] < self.sma[0]
        elif self.params.ma_strategy_enum == MaStrategyEnum.MMA:
            return self.sma_cross < 0
        elif self.params.ma_strategy_enum == MaStrategyEnum.EMA:
            return self.dataclose[0] < self.ema[0]
        else:
            return self.ema_cross < 0
        
    def next(self):
        self.log('MaStrategy Close, %.2f' % self.dataclose[0])

        # 如果之前已经有订单在处理，但是还没处理完，就不再处理新订单 ( 这是当前策略处理的逻辑 )
        if self.order:
            return

        # 手里是否有头寸, 如果没有头寸就处理只处理买逻辑, 如果有头寸就处理卖逻辑
        dt = self.data.datetime.date(0).strftime("%Y-%m-%d")
        if not self.position:
            if self.can_buy():
                max_price_size = self.get_max_size()
                rise = (self.dataclose[0] - self.dataclose[-1]) / self.dataclose[0]
                print(rise)
                if rise > 0.9:
                    price = self.dataclose[0] * (1 + 0.05)
                    max_price_size = math.floor(self.broker.get_cash() / 100 / price) * 100
                print('%s : buy price: %.2f size: %d' % (dt, self.dataclose[0], max_price_size))

                self.log('BUY CREATE , %.4f, %.1f' %
                         (self.dataclose[0], max_price_size))

                self.order = self.buy(size=max_price_size)
        else:
            if self.can_sell():
                print('%s : sell price: %.2f size: %d' % (dt, self.dataclose[0], self.position.size))
                self.order = self.sell(size=self.position.size)

        # 获取当前的总价值
        self.value = self.broker.getvalue()

    def stop(self):
        dt2 = None
        dt2 = dt2 or self.datas[0].datetime.date(0)
        print('%s : End (SMA period %d) Portfolio Value: %.2f' %
              (dt2.isoformat(), self.params.maperiod, self.value))

    def get_strategy_config() -> StrategyConfigBase:
        cfg = TdxStrategyConfigImpl()
        cfg.set_plot(True)
        cfg.set_data_path('E:/projects/pystock/pystock/tdx/data/tdx/day/sh600026.csv')
        cfg.set_start_date(datetime.now() - relativedelta(years=3))
        cfg.set_end_date(datetime.now())
        return cfg

# if __name__ == '__main__':
#     print(TestStrategyPlanA.__name__ + ' version:'+TestStrategyPlanA.__version__)
