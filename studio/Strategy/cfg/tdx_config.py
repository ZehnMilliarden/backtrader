import studio.Strategy.strategy_config as strategy_config
import backtrader
import pandas
from datetime import datetime


class TdxStrategyConfigImpl(strategy_config.StrategyConfigBase):

    def __init__(self):
        self.__is_plot__ = False
        self.__start_date__ = datetime(2014, 1, 1)
        self.__end_date__ = datetime(2014, 12, 31)
        self.__data_path__ = 'datas/TDXStock/tdx/day/sh000001.csv'

    def is_plot(self) -> bool:
        return self.__is_plot__

    def set_plot(self, is_plot: bool):
        self.__is_plot__ = is_plot

    def get_stock_data(self) -> backtrader.feeds.PandasData:

        # 数据格式
        # datafields = [
        #   'datetime', 'open', 'high', 'low', 'close', 'volume', 'openinterest'
        # ]

        stock_data_raw = pandas.read_csv(
            self.get_data_path(), index_col='date', parse_dates=True)

        start_date = self.get_start_date()
        end_date = self.get_end_date()

        stock_data = backtrader.feeds.PandasData(
            dataname=stock_data_raw, fromdate=start_date, todate=end_date)

        return stock_data

    def get_start_date(self) -> datetime:
        return self.__start_date__

    def set_start_date(self, start_date: datetime):
        self.__start_date__ = start_date

    def get_end_date(self) -> datetime:
        return self.__end_date__

    def set_end_date(self, end_date: datetime):
        self.__end_date__ = end_date

    def get_data_path(self) -> str:
        return self.__data_path__

    def set_data_path(self, data_path: str):
        self.__data_path__ = data_path

    def get_exit_bar(self) -> int:
        return 20 * 12 * 3
