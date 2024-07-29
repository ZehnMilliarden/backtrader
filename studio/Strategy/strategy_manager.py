from studio.Strategy.default_strategy import TestStrategyDefault
from studio.Strategy.demo.test_strategy_c import TestStrategyPlanC
from studio.Strategy.demo.test_strategy_a import TestStrategyPlanA
from studio.Strategy.demo.test_strategy_b import TestStrategyPlanB
from studio.Strategy.ma.ma_strategy import MaStrategy
from studio.Strategy.trend.trend_strategy import TrendStrategy


class TestStrategyManager:

    __version__ = '1.0'

    def __init__(self):
        self.__StrategyType = TestStrategyDefault.__name__

    def SetStrategy(self, StrategyType):
        self.__StrategyType = StrategyType

    def GetStrategy(self):
        if self.__StrategyType == TestStrategyDefault.__name__:
            return TestStrategyDefault
        elif self.__StrategyType == TestStrategyPlanA.__name__:
            return TestStrategyPlanA
        elif self.__StrategyType == TestStrategyPlanB.__name__:
            return TestStrategyPlanB
        elif self.__StrategyType == TestStrategyPlanC.__name__:
            return TestStrategyPlanC
        elif self.__StrategyType == MaStrategy.__name__:
            return MaStrategy
        elif self.__StrategyType == TrendStrategy.__name__:
            return TrendStrategy
        return TestStrategyDefault

# if __name__ == '__main__':
#     print(TestStrategyManager.__name__ + ' version:' + TestStrategyManager.__version__)
