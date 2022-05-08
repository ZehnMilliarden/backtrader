
from __future__ import (absolute_import, division, print_function, unicode_literals)

from .runtime import CurrentWorkPath as cw
cw.AddProjectFolderToWorkPath()

import backtrader
import pandas
from datetime import datetime

from .strategy_manager import TestStrategyManager

class TestManager():

    __version__ = '1.0'

    def run(strategy_name):
        cerebro = backtrader.Cerebro()

        strategyManager = TestStrategyManager()
        strategyManager.SetStrategy(strategy_name)

        cerebro.addstrategy(strategyManager.GetStrategy())

        stock_data_raw = pandas.read_csv(
            'datas\yhoo-2014.txt', index_col='Date', parse_dates=True)
        # print(stock_data_raw)

        start_date = datetime(2014, 1, 2)
        end_date = datetime(2014, 12, 31)

        stock_data = backtrader.feeds.PandasData(
            dataname=stock_data_raw, fromdate=start_date, todate=end_date)

        cerebro.adddata(stock_data)

        cerebro.broker.setcash(100000.0)

        print('Starting Portfolio Value: %.2f' % cerebro.broker.getvalue())
        cerebro.run()
        print('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())

# if __name__ == '__main__':
#     print(TestManager.__name__ + ' version:' + TestManager.__version__)