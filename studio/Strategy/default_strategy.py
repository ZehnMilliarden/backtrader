import imp
import pandas
import backtrader
from datetime import datetime
from typing import overload
from Strategy.strategy_config import StrategyConfigBase
from Strategy.demo.test_strategy_config import TestStrategyConfigImpl
import math


class TestStrategyDefault(backtrader.Strategy):

    __version__ = '1.0'

    __need_log = False

    def log(self, txt, dt=None):
        ''' 提供记录功能 '''
        if (self.__need_log == False):
            return

        dt = dt or self.datas[0].datetime.date(0)
        print('%s, %s' % (dt.isoformat(), txt))

    def __init__(self):
        # 引用到 输入数据的close价格
        self.log('TestStrategyDefault __init__')
        self.dataclose = self.datas[0].close
        self.dataopen = self.datas[0].open
        self.datahight = self.datas[0].high
        self.datalow = self.datas[0].low
        self.datavolume = self.datas[0].volume

    def set_need_log(self, need_log):
        self.__need_log == need_log

    def get_strategy_config() -> StrategyConfigBase:
        cfg = TestStrategyConfigImpl()
        return cfg

    def get_max_size(self, value):
        return math.floor(
            self.broker.get_cash() / 100 / value) * 100

    def get_next_open(self) -> float:
        try:
            return self.datasopen[1]
        except:
            return 0.0
        # if __name__ == '__main__':
        #     print( TestStrategyDefault.__name__ + ' version:' + TestStrategyDefault.__version__)
