
from pandas import Period
import backtrader
from .default_strategy import TestStrategyDefault


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
        data0Slice = self.data.get(0, 5)
        print(data0Slice)

    def next(self):
        self.test_data()
