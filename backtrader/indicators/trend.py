from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

from . import Indicator, Average
from . import CrossOver
import math
import numpy


class TrendHelp(Indicator):

    alias = ('TrendHelp', )
    params = {'period_fast': 10, 'period_slow': 20}
    lines = ('fast', 'slow', )
    plotinfo = dict(subplot=False)

    def __init__(self) -> None:
        self.lines.fast = Average(
            self.data.close, period=self.params.period_fast)
        self.lines.slow = Average(
            self.data.close, period=self.params.period_slow)
        self.slope_fast = numpy.full(len(self.data.close.array), numpy.nan)
        self.slope_slow = numpy.full(len(self.data.close.array), numpy.nan)
        self.cross = CrossOver(
            self.lines.fast, self.lines.slow)
        super(TrendHelp, self).__init__()

    def once(self, start, end):
        self._CaclSlope(start, end)

    def advance(self, size=1):
        self.slope_fast = numpy.roll(self.slope_fast, -1)
        self.slope_slow = numpy.roll(self.slope_slow, -1)
        self.cross = numpy.roll(self.cross, -1)
        return super().advance(size)

    def _CaclSlope(self, start, end):
        for index in range(start, end):
            if index == start:
                continue
            self.slope_slow[index] = (self.lines.slow[index] -
                                      self.lines.slow[index-1]) / self.lines.slow[index-1]
            self.slope_fast[index] = (self.lines.fast[index] -
                                      self.lines.fast[index-1]) / self.lines.fast[index-1]


class Trend(Indicator):

    alias = ('Trend', )
    params = {'period_fast': 10, 'period_slow': 20}
    plotinfo = dict(subplot=False)
    lines = ('trend_0', 'trend_1',)
    _first_index: int = 0

    def __init__(self):
        self.trendHelp = TrendHelp(
            self.data, period_fast=self.params.period_fast, period_slow=self.params.period_slow)
        super(Trend, self).__init__()

    def _findpreIndex(self) -> int:
        index: int = -1
        while True:
            if index < self._first_index:
                break
            if self.trendHelp.cross[index] != 0.0:
                return index
            index = index - 1
        return 0

    def next(self):
        indexpre = self._findpreIndex()
        if indexpre != 0:
            self._CaclLines(indexpre, 0)

    def advance(self, size=1):
        self._first_index = self._first_index - size
        return super().advance(size)

    def _ConveHullImpl(self, potLine) -> list():
        pass

    def _ConvexHull(self):
        self.trendLineSet = list()
        for potLine in self.potLineSet:
            trendLine = list()
            self.trendLineSet.append(self._ConveHullImpl(trendLine))

    def _CaclLines(self, start, end) -> None:
        if self.trendHelp.cross[start] > 0:
            currentLine = self.lines.trend_0  # 上升线
        elif self.trendHelp.cross[start] < 0:
            currentLine = self.lines.trend_1  # 上升线
        else:
            return

        currentLine[start] = self.data.close[start]
        for index in range(start + 1, end):
            currentLine[index] = currentLine[index-1]
