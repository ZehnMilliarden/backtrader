
from pandas import Period
import backtrader
from Strategy.default_strategy import TestStrategyDefault
from datetime import datetime
import pandas
from Strategy.strategy_config import StrategyConfigBase
from Strategy.cfg.tdx_config import TdxStrategyConfigImpl
import math
from dateutil.relativedelta import relativedelta


class MaStrategy(TestStrategyDefault):

    # 外部传参
    params = {
        "exit_bar": 5,
        "maperiod": 20
    }

    def __init__(self):
        # order 用于标记 当前正在处理的订单\
        super(MaStrategy, self).__init__()

        self.order = None

        self.sma = backtrader.indicators.SMA(
            self.dataclose, period=28)

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
            # 订单 保证金不足（现金不足）
            self.log('Order %s', order.Margin.__str__)

        self.order = None

    def next(self):
        self.log('MaStrategy Close, %.2f' % self.dataclose[0])

        # 如果之前已经有订单在处理，但是还没处理完，就不再处理新订单 ( 这是当前策略处理的逻辑 )
        if self.order:
            return

        try:
            current_data_close = self.dataclose[0]
            current_sma = self.sma[0]
            pre_data_close = self.dataclose[-1]
            pre_sma = self.sma[-1]
            next_data_open = self.dataopen[1]
        except:
            return

        # 手里是否有头寸, 如果没有头寸就处理只处理买逻辑, 如果有头寸就处理卖逻辑
        if not self.position:

            if (current_data_close > current_sma) and (pre_data_close <= pre_sma):

                self.log('MaStrategy buy create: %.2f, sma[0]:%.2f'
                         % (current_data_close, current_sma))

                buyvalue = max(current_data_close, next_data_open)

                max_price_size = self.get_max_size(buyvalue)

                self.log('BUY CREATE , %.4f, %.1f' %
                         (buyvalue, max_price_size))

                self.order = self.buy(size=max_price_size)

        else:
            if current_data_close < current_sma:
                self.log('MaStrategy sell create: %.2f, sma[0]:%.2f' %
                         (current_data_close, current_sma))
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
        cfg.set_data_path('datas/TDXStock/tdx/day/sh600025.csv')
        cfg.set_start_date(datetime.now() - relativedelta(years=3))
        cfg.set_end_date(datetime.now())
        return cfg

# if __name__ == '__main__':
#     print(TestStrategyPlanA.__name__ + ' version:'+TestStrategyPlanA.__version__)
