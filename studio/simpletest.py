
# https://blog.csdn.net/h00cker/category_11448348.html
# https://zhuanlan.zhihu.com/p/368044337

from Strategy.test_manager import TestManager
from Strategy.test_strategy_b import TestStrategyPlanB
from Strategy.test_strategy_a import TestStrategyPlanA

if __name__ == '__main__':
    testManager = TestManager()
    testManager.set_strategy_name(TestStrategyPlanA.__name__)
    testManager.set_data_path('datas\yhoo-2014.txt')
    testManager.set_commission(0.001)
    testManager.set_stake_size(100)
    testManager.run()
