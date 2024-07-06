
from __future__ import (absolute_import, division,
                        print_function, unicode_literals)
from .default_strategy import TestStrategyDefault
from .strategy_manager import TestStrategyManager
from datetime import datetime
import pandas
import backtrader


class TestManager():

    __version__ = '1.0'

    __strategy_name = TestStrategyDefault.__name__

    __data_path = 'datas\yhoo-2014.txt'

    __commission = 0.0005

    __stake_size = 100

    def set_stake_size(self, stake_size):
        self.__stake_size = stake_size
        return True

    def set_strategy_name(self, strategy_name):
        self.__strategy_name = strategy_name
        return True

    def set_data_path(self, data_name):
        self.__data_path = data_name
        return True

    def set_commission(self, commission):
        self.__commission = commission
        return True

    def run(self):
        cerebro = backtrader.Cerebro()

        strategyManager = TestStrategyManager()
        strategyManager.SetStrategy(self.__strategy_name)

        # 添加策略
        cerebro.addstrategy(strategyManager.GetStrategy(), exit_bar=90)

        # cerebro.optstrategy(strategyManager.GetStrategy(),
        #                     maperiod=range(15, 25))

        stock_data_raw = pandas.read_csv(
            self.__data_path, index_col='Date', parse_dates=True)
        # print(stock_data_raw)

        start_date = datetime(2014, 1, 2)
        end_date = datetime(2014, 12, 31)

        stock_data = backtrader.feeds.PandasData(
            dataname=stock_data_raw, fromdate=start_date, todate=end_date)

        # 添加测试数据
        cerebro.adddata(stock_data)

        # 本金设置
        cerebro.broker.setcash(100000.0)

        # 佣金设置
        cerebro.broker.setcommission(self.__commission)

        # 设置股票数量(每手)
        cerebro.addsizer(backtrader.sizers.FixedSize, stake=self.__stake_size)

        print('Starting Portfolio Value: %.2f' % cerebro.broker.getvalue())
        cerebro.run()
        print('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())

        # 可视化画图, 有引入问题, 暂时屏蔽
        cerebro.plot()

        return True
# if __name__ == '__main__':
#     print(TestManager.__name__ + ' version:' + TestManager.__version__)
