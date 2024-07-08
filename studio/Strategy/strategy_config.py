import backtrader
import pandas
from datetime import datetime
from typing import overload


class StrategyConfigBase(object):

    @overload
    def is_plot(self) -> bool: ...

    @overload
    def get_stock_data(self) -> backtrader.feeds.PandasData: ...

    @overload
    def get_start_date(self) -> datetime: ...

    @overload
    def get_end_date(self) -> datetime: ...

    @overload
    def get_data_path(self) -> str: ...

    @overload
    def get_exit_bar(self) -> int: ...
