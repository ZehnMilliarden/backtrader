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

    def _directed_area(self, m):
        return (m[2]['index'] - m[0]['index']) * (m[1]['val'] - m[0]['val']) - (m[1]['index'] - m[0]['index']) * (m[2]['val'] - m[0]['val'])

    def _convex_hull(self,  point_list, direct):
        '''
        Input:  Given a point List: A List of Truple (x,y)
        Output: Return a point list: A List of Truple (x,y) which is CONVEX HULL of input
        For the sake of effeciency, There is no error check mechanism here. Please catch outside
        '''
        n = len(point_list)  # Total Length
        # point_list.sort()

        # Valid Check:
        if n < 3:
            return point_list

        potSet = list()

        # Building Upper Hull: Initialized with first two point
        if direct:
            potSet = point_list[0:1]
            for i in range(2, n):
                potSet.append(point_list[i])
                while len(potSet) >= 3 and not self._directed_area(potSet[-3:]):
                    del potSet[-2]
        else:
            # Building Lower Hull: Initialized with last two point
            potSet = [point_list[-1], point_list[-2]]
            for i in range(n - 3, -1, -1):  # From the i-3th to the first point
                potSet.append(point_list[i])
                while len(potSet) >= 3 and not self._directed_area(potSet[-3:]):
                    del potSet[-2]
            potSet.reverse()
        return potSet

    def _ConvexHull(self, potLine, trendLine, direct) -> list:
        pots = list()
        for index,  pot in enumerate(potLine):
            if direct:
                pots.append(
                    {'index': pot['index'], 'val': pot['low']})
            else:
                pots.append(
                    {'index': pot['index'], 'val': pot['high']})
        trendPots = self._convex_hull(pots, direct)
        for index, pot in enumerate(trendPots):
            if index == 0:
                continue
            prePot = trendPots[index-1]
            k = (pot['val'] - prePot['val']) / (pot['index'] - prePot['val'])
            for potIndex in range(prePot['index'], pot['index']):
                trendLine[potIndex] = prePot['val'] + k
        return trendLine

    def _CaclLines(self, start, end) -> None:
        if self.trendHelp.cross[start] > 0:
            currentLine = self.lines.trend_0  # 上升线
        elif self.trendHelp.cross[start] < 0:
            currentLine = self.lines.trend_1  # 上升线
        else:
            return

        potLine = list()
        for index in range(start, end):
            potLine.append(
                {'index': index, 'high': self.data.high[index], 'low': self.data.low[index]})
        self._ConvexHull(potLine, currentLine,
                         currentLine == self.lines.trend_0)
