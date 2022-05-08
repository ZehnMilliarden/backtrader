
from .default_strategy import TestStrategyDefault

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

# if __name__ == '__main__':
#     print(TestStrategyPlanA.__name__ + ' version:'+TestStrategyPlanA.__version__)