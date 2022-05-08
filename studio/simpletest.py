
# https://blog.csdn.net/h00cker/category_11448348.html

from Strategy.test_manager import TestManager
from Strategy.test_strategy_b import TestStrategyPlanB

if __name__ == '__main__':
    testManager = TestManager()
    testManager.set_strategy_name(TestStrategyPlanB.__name__)
    testManager.set_data_path('datas\yhoo-2014.txt')
    testManager.run()