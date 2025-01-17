
# https://blog.csdn.net/h00cker/category_11448348.html
# https://zhuanlan.zhihu.com/p/368044337

from Strategy.test_manager import TestManager
from Strategy.demo.test_strategy_b import TestStrategyPlanB
from Strategy.demo.test_strategy_a import TestStrategyPlanA
from Strategy.demo.test_strategy_c import TestStrategyPlanC
from Strategy.ma.ma_strategy import MaStrategy

if __name__ == '__main__':
    testManager = TestManager()
    testManager.set_strategy_name(MaStrategy.__name__)
    testManager.set_commission(0.0005)
    testManager.set_stake_size(100)
    testManager.run()
