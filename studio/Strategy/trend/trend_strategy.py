from pandas import Period
import backtrader
from Strategy.default_strategy import TestStrategyDefault
from datetime import datetime
import pandas
from Strategy.strategy_config import StrategyConfigBase
from Strategy.cfg.tdx_config import TdxStrategyConfigImpl
import math
from dateutil.relativedelta import relativedelta


class TrendStrategy(TestStrategyDefault):

    params = {
        "exit_bar": 5,
        "maperiod": 20,
    }

    def __init__(self):
        super(TrendStrategy, self).__init__()

    def get_strategy_config() -> StrategyConfigBase:
        cfg = TdxStrategyConfigImpl()
        cfg.set_plot(True)
        cfg.set_data_path(
            'datas/TDXStock/tdx/day/sh600026.csv')
        cfg.set_start_date(datetime.now() - relativedelta(years=3))
        cfg.set_end_date(datetime.now())
        return cfg

    def next(self):
        pass
