
from pandas import Period
import backtrader
from .default_strategy import TestStrategyDefault


class TestStrategyPlanA(TestStrategyDefault):

    # 外部传参
    params = (
        ("exitbars", 5),
        ("maperiod", 20)
    )

    def __init__(self):
        # 引用到 输入数据的close价格
        TestStrategyDefault.__init__(self)

        # order 用于标记 当前正在处理的订单
        self.order = None

        # 移动均线
        self.sma = backtrader.indicators.MovingAverageSimple(
            self.datas[0], period=self.params.maperiod)

        # 移动均线
        self.sma = backtrader.indicators.SMA(
            self.datas[0], period=self.params.maperiod)

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

                self.log('TestStrategyPlanA buy execute Size:%d Price: %.2f, Cost: %.2f, Comm: %.2f, period: %d' %
                         (order.executed.size,
                          order.executed.price,
                          order.executed.value,
                          order.executed.comm,
                          self.params.maperiod))

            elif order.issell():

                # 同上

                self.log('TestStrategyPlanA sell execute Size:%d Price: %.2f, Cost: %.2f, Comm: %.2f, period: %d' %
                         (order.executed.size,
                          order.executed.price,
                          order.executed.value,
                          order.executed.comm,
                          self.params.maperiod))

            else:
                self.log('TestStrategyPlanA unrecorgnized order: %s' %
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
        # self.log('TestStrategyPlanA Close, %.2f' % self.dataclose[0])

        # 如果之前已经有订单在处理，但是还没处理完，就不再处理新订单 ( 这是当前策略处理的逻辑 )
        if self.order:
            return

        # 手里是否有头寸, 如果没有头寸就处理只处理买逻辑, 如果有头寸就处理卖逻辑
        if not self.position:

            if self.dataclose[0] >= self.sma[0]:
                # 连续下跌两天就买入
                self.log('TestStrategyPlanA buy create: %.2f, sma[0]:%.2f'
                         % (self.dataclose[0], self.sma[0]))
                self.order = self.buy()
        else:

            # len(self) 记录最后一次执行bar的位置, 每次next会加1, bar_executed记录上次进行交易完成的 bar 位置
            # 距离上次交易 过去了exitbars个 bar 时间单位(在这里一个bar是一天), 就直接执行出售
            if self.dataclose[0] < self.sma[0]:
                self.log('TestStrategyPlanA sell create: %.2f, sma[0]:%.2f' %
                         (self.dataclose[0], self.sma[0]))
                self.order = self.sell()

    # 这里有个崩溃问题
    # def stop(self):
    #     dt2 = dt2 or self.datas[0].datetime.date(0)
    #     print('%s : End (SMA period %d) Portfolio Value: %.2f' %
    #           (dt2.isoformat(), self.params.maperiod, self.value))

# if __name__ == '__main__':
#     print(TestStrategyPlanA.__name__ + ' version:'+TestStrategyPlanA.__version__)
