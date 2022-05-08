
# https://blog.csdn.net/h00cker/category_11448348.html

from Strategy.test_manager import TestManager
from Strategy.test_strategy_b import TestStrategyPlanB

if __name__ == '__main__':
    TestManager.run(TestStrategyPlanB.__name__)