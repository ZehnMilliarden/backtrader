
from pandas import Period
import backtrader
from backtrader.indicators import sma
from Strategy.default_strategy import TestStrategyDefault
from Strategy.strategy_config import StrategyConfigBase
from Strategy.demo.test_strategy_config import TestStrategyConfigImpl

class TestStrategyPlanC(TestStrategyDefault):

    params = {
        "need_log": False,
        "exit_bar": 20,
        "period": 20}

    def __init__(self):
        super().__init__()
        super().set_need_log(self.params.need_log)

        self.sma = backtrader.indicators.SMA(
            self.datas[0], period=self.params.period)

        close_over_sma = self.dataclose > self.sma

        self.sma_dist_to_high = self.data.high - self.sma

        sma_dist_small = self.sma_dist_to_high < 3.5

        self.sell_sig = backtrader.And(close_over_sma, sma_dist_small)

    def test_data(self):

        # xxx.lines.name可以简化为xxx.lines_name
        # self.data_name 等于 self.data.lines.name
        # 如果有多个变量的话，也可以self.data1_name 替代self.data1.lines.name

        # xxx.line = xxx.lines[0]
        # xxx.line[X] = xxx.lineX = xxx.line_X
        # self.dataY = self.data.lineY
        # self.dataX_Y = self.data[X].line[Y] = self.dataX.line[Y]

        print("LINES.CLOSE:%.2f, %.2f, SMA:%.2f" % (
            self.datas[0].lines.close[0],
            self.data0_close[0],
            self.sma.lines.sma[0]
        ))

        # 获取 -4 到 0 的切片数据, x-y+1 -> x 的数据
        data0_Slice = self.data.get(0, 5)
        print(data0_Slice)

    def log_v1(self):
        if self.sma > 30.0:
            print('sma %.2f is greater than 30.0' % self.sma[0])
        if self.sma > self.data.close:
            print('sma %.2f is above the close price %.2f' %
                  (self.sma[0], self.dataclose[0]))
        if self.sell_sig:  # if sell_sig == True: 这种写法也可以
            print('sell sig is True')
        else:
            print('sell sig is False')
        if self.sma_dist_to_high > 5.0:
            print('distance from sma to hig is greater than 5.0')

    def next(self):
        self.test_data()
        self.log_v1()