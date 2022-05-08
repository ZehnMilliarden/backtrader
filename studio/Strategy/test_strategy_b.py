
from .default_strategy import TestStrategyDefault

class TestStrategyPlanB(TestStrategyDefault):

    def __init__(self):
        # 引用到 输入数据的close价格
        TestStrategyDefault.__init__(self)
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

            # 执行完毕的订单 数量, 不区分购买还是出售订单
            self.bar_executed = len(self)

        elif order.status in [order.Canceled, order.Rejected, order.Margin]:
            # 订单 取消, 拒绝, 或保证金订单?
            self.log('Order %s', order.status)
        
        self.order=None

    def next(self):
        # self.log('TestStrategyPlanB Close, %.2f' % self.dataclose[0])

        if self.order:
            return

        if not self.position:

            if self.dataclose[0] < self.dataclose[-1] and self.dataclose[-1] < self.dataclose[-2]:
                # 连续下跌两天就买入
                self.log('TestStrategyPlanB buy create %.2f, dataclose[-1]:%.2f, dataclose[-2]:%.2f' 
                    % ( self.dataclose[0], self.dataclose[-1], self.dataclose[-2]))
                self.buy()
        else:
            
            if len(self) >= self.bar_executed+5:
                self.log('TestStrategyPlanB sell create %.2f' % self.dataclose[0])
                self.order = self.sell()

# if __name__ == '__main__':
#     print(TestStrategyPlanB.__name__ + ' version:'+TestStrategyPlanB.__version__)