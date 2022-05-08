
from .default_strategy import TestStrategyDefault

class TestStrategyPlanB(TestStrategyDefault):

    def __init__(self):
        # 引用到 输入数据的close价格
        TestStrategyDefault.__init__(self)

        #order 用于标记 当前正在处理的订单
        self.order = None

    # 订单状态变更
    def notify_order(self, order):
        if order.status in [order.Submitted, order.Accepted]:
            # 订单状态处于，提交订单, 订单被接受
            return
        
        if order.status in [order.Completed]:
            if order.isbuy():
                self.log('TestStrategyPlanB buy execute: %.2f' % order.executed.price)
            elif order.issell():
                self.log('TestStrategyPlanB sell execute: %.2f' % order.executed.price)
            else:
                self.log('TestStrategyPlanB unrecorgnized order: %s' % order.status)

            # 执行完毕的订单 bar 的位置, 不区分购买还是出售订单
            self.bar_executed = len(self)

        elif order.status in [order.Canceled, order.Rejected, order.Margin]:
            # 订单 取消, 拒绝, 或保证金订单?
            self.log('Order %s', order.status)
        
        self.order=None

    def next(self):
        # self.log('TestStrategyPlanB Close, %.2f' % self.dataclose[0])

        # 如果之前已经有订单在处理，但是还没处理完，就不再处理新订单 ( 这是当前策略处理的逻辑 )
        if self.order:
            return

        # 手里是否有头寸, 如果没有头寸就处理只处理买逻辑, 如果有头寸就处理卖逻辑
        if not self.position:

            if self.dataclose[0] < self.dataclose[-1] and self.dataclose[-1] < self.dataclose[-2]:
                # 连续下跌两天就买入
                self.log('TestStrategyPlanB buy create: %.2f, dataclose[-1]:%.2f, dataclose[-2]:%.2f' 
                    % ( self.dataclose[0], self.dataclose[-1], self.dataclose[-2]))
                self.order = self.buy()
        else:
            
            # len(self) 记录最后一次执行bar的位置, 每次next会加1, bar_executed记录上次进行交易完成的 bar 位置
            # 距离上次交易 过去了5个 bar 时间单位(在这里一个bar是一天), 就直接执行出售
            if len(self) >= self.bar_executed+5:
                self.log('TestStrategyPlanB sell create: %.2f' % self.dataclose[0])
                self.order = self.sell()

# if __name__ == '__main__':
#     print(TestStrategyPlanB.__name__ + ' version:'+TestStrategyPlanB.__version__)