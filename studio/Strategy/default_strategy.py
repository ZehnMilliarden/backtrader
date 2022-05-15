import imp
import pandas
import backtrader


class TestStrategyDefault(backtrader.Strategy):

    __version__ = '1.0'

    def log(self, txt, dt=None):
        ''' 提供记录功能 '''
        dt = dt or self.datas[0].datetime.date(0)
        print('%s, %s' % (dt.isoformat(), txt))

    def __init__(self):
        # 引用到 输入数据的close价格
        self.log('TestStrategyDefault __init__')
        self.dataclose = self.datas[0].close

    def next(self):
        self.log('TestStrategyDefault Close, %.2f' % self.dataclose[0])

# if __name__ == '__main__':
#     print( TestStrategyDefault.__name__ + ' version:' + TestStrategyDefault.__version__)
