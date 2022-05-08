
from .default_strategy import TestStrategyDefault
from .test_strategy_a import TestStrategyPlanA
from .test_strategy_b import TestStrategyPlanB

class TestStrategyManager:

    __version__ = '1.0'

    def __init__(self):
        self.__StrategyType = TestStrategyDefault.__name__

    def SetStrategy(self, StrategyType):
        self.__StrategyType=StrategyType

    def GetStrategy(self):
        if self.__StrategyType == TestStrategyDefault.__name__:
            return TestStrategyDefault
        elif self.__StrategyType == TestStrategyPlanA.__name__:
            return TestStrategyPlanA
        elif self.__StrategyType == TestStrategyPlanB.__name__:
            return TestStrategyPlanB
        return TestStrategyDefault

# if __name__ == '__main__':
#     print(TestStrategyManager.__name__ + ' version:' + TestStrategyManager.__version__)