from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

from . import Indicator, Average
from . import CrossOver
import math


class Trend(Indicator):

    alias = ('Trend', )
    params = {'period_fast': 10, 'period_slow': 20}
    plotinfo = dict(subplot=False)
    lines = ('fast', 'slow', 'trend',)

    def __init__(self):
        self.lines.fast = Average(self.data, period=self.params.period_fast)
        self.lines.slow = Average(self.data, period=self.params.period_slow)
        self.cross = CrossOver(
            self.lines.fast, self.lines.slow)
        self.dst = self.lines.trend.array
        super(Trend, self).__init__()

    def next(self):
        self.lines.trend.array[0] = self.data[0]

    def once(self, start, end):
        for index, crs in enumerate(self.cross):
            if index in range(start, end):
                if math.isnan(crs):
                    self.lines.trend[index] = 0.0
                elif crs != 0:
                    self.lines.trend[index] = self.data[index]
                else:
                    self.lines.trend[index] = self.lines.trend[index - 1]
