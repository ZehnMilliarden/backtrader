from __future__ import absolute_import, division, print_function, unicode_literals

from . import Indicator, Highest, Lowest
from ..utils import num2date
import datetime


class HighLowIndicator(Indicator):
    lines = ("highest", "lowest")
    params = (
        ("start_date", datetime.datetime(2020, 3, 1)),
        ("end_date", datetime.datetime(2020, 9, 1)),
    )

    plotinfo = dict(subplot=False)

    def __init__(self):
        self.in_range = False
        self.high_values = []
        self.low_values = []

    def next(self):
        current_date = num2date(self.data.datetime[0])

        # 判断当前日期是否在指定时间范围内
        if self.params.start_date <= current_date <= self.params.end_date:
            if not self.in_range:
                self.in_range = True
                self.high_values = []  # 进入范围时清空之前存储的值
                self.low_values = []
            self.high_values.append(self.data.high[0])
            self.low_values.append(self.data.low[0])

            # 计算当前范围内的最高和最低股价
            self.lines.highest[0] = max(self.high_values)
            self.lines.lowest[0] = min(self.low_values)
        else:
            if self.in_range:
                self.in_range = False
                self.high_values = []  # 离开范围时清空存储的值
                self.low_values = []
            self.lines.highest[0] = float("nan")  # 不在范围内时设为 NaN
            self.lines.lowest[0] = float("nan")
