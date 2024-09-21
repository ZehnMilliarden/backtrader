
from __future__ import (absolute_import, division,
                        print_function, unicode_literals)
from .default_strategy import TestStrategyDefault
from .strategy_manager import TestStrategyManager
from datetime import datetime
import pandas
import backtrader
from Strategy.strategy_config import StrategyConfigBase
from Strategy.demo.test_strategy_config import TestStrategyConfigImpl
import os
import sys


class TestManager():

    __version__ = '1.0'

    __strategy_name = TestStrategyDefault.__name__

    __commission = 0.0005

    __stake_size = 100

    def set_stake_size(self, stake_size):
        self.__stake_size = stake_size
        return True

    def set_strategy_name(self, strategy_name):
        self.__strategy_name = strategy_name
        return True

    def set_commission(self, commission):
        self.__commission = commission
        return True

    def run_once(self, dt_file):
        cerebro = backtrader.Cerebro()

        strategyManager = TestStrategyManager()
        strategyManager.SetStrategy(self.__strategy_name)

        test_stategy = strategyManager.GetStrategy()
        strategy_config = test_stategy.get_strategy_config()
        strategy_config.set_data_path(dt_file)

        # 添加策略
        cerebro.addstrategy(
            test_stategy, exit_bar=strategy_config.get_exit_bar())
        #cerebro.optstrategy(test_stategy, maperiod=range(15, 50))

        # cerebro.optstrategy(strategyManager.GetStrategy(),
        #                     maperiod=range(15, 25))

        # 添加测试数据
        cerebro.adddata(strategy_config.get_stock_data())

        # 设置
        cerebro.broker.setcash(100000.0)

        # 佣金设置
        cerebro.broker.setcommission(self.__commission)

        # 设置数量
        cerebro.addsizer(backtrader.sizers.FixedSize, stake=self.__stake_size)

        res = [cerebro.broker.getvalue()]
        #print('Starting Portfolio Value: %.2f' % cerebro.broker.getvalue())
        cerebro.run()
        #print('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())
        res.append(cerebro.broker.getvalue())

        # 可视化画图, 有引入问题, 暂时屏蔽
        #if strategy_config.is_plot() is True:
            #cerebro.plot(style='candle',
                         #barup='red', bardown='green')
        return res

    def run(self):
        
        tt = 0
        c = 0
        dc = 0
        dir = 'D:/Workspace/backtrader/datas/tdx/'
        file_list = os.listdir(dir)
        h = open('macd_var.txt', 'w')
        for f in file_list:
            #tf = os.path.abspath(f)
            tf = os.path.join(dir, f)
            code: str = f.split('.')[0][2:]

            res = self.run_once(tf)

            sys.stdout = h
            final = res[1] - res[0]
            result = 'increase'
            c += 1
            if final <= 0:
                result = 'decrease'
                dc += 1
            print(code,'\t%.2f' % final,'\t',result)
            sys.stdout = sys.__stdout__

            tt += final
        
        ic = c - dc
        sys.stdout = h
        print('%.2f\t' % tt,'%d\t' % c,'%d\t'% ic ,'%d' % dc)
        sys.stdout = sys.__stdout__

        print('%.2f\t' % tt,'%d\t' % c,'%d\t'% ic ,'%d' % dc)

        h.close()

        return True
# if __name__ == '__main__':
#     print(TestManager.__name__ + ' version:' + TestManager.__version__)
