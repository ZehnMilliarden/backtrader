from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

from . import Indicator, Average
from . import CrossOver
import math


class Trend(Indicator):

    alias = ('Trend', )
    params = {'period_fast': 10, 'period_slow': 20}
    plotinfo = dict(subplot=False)
    lines = ('fast', 'slow', 'trend_0', 'trend_1',)

    def __init__(self):
        self.lines.fast = Average(self.data, period=self.params.period_fast)
        self.lines.slow = Average(self.data, period=self.params.period_slow)
        self.cross = CrossOver(
            self.lines.fast, self.lines.slow)
        super(Trend, self).__init__()

    def next(self):
        self.lines.trend_0[0] = self.data[0]
        self.lines.trend_1[0] = self.data[0]

    def once(self, start, end):
        currentLine = self.lines.trend_0
        preLine = self.lines.trend_1
        for index, crs in enumerate(self.cross):
            if index in range(start, end):
                if math.isnan(crs):
                    self.lines.trend_0[index] = crs
                    self.lines.trend_1[index] = crs
                elif crs != 0:
                    if currentLine is self.lines.trend_0:
                        currentLine = self.lines.trend_1
                        preLine = self.lines.trend_0
                    else:
                        currentLine = self.lines.trend_0
                        preLine = self.lines.trend_1
                    currentLine[index] = self.data[index]
                else:
                    if math.isnan(currentLine[index-1]):
                        currentLine[index] = preLine[index-1]
                    else:
                        currentLine[index] = currentLine[index-1]

    def _ConvexHull(self):
        pass
