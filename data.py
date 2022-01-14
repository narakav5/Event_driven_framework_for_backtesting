# -*- coding: utf-8 -*-

# data.py

from abc import ABCMeta, abstractmethod
import os
import os.path

import numpy as np
import pandas as pd
import talib

from event import MarketEvent


class DataHandler(object):
    """
    DataHandler是一个抽象基类提供所有后续的数据处理类的接口（包括历史和
    实际数据处理）
    （衍生的）数据处理对象的目标是输出一组针对每个请求的代码的数据条
    （OHLCVI），以这样的方式来模拟实际的交易策略并发送市场信号。
    在后续的回测当中，历史数据和实际交易采用相同的方式。
    """
    __metaclass__ = ABCMeta

    # @abstractmethod
    # def get_latest_bar(self, symbol):
    #     """
    #     返回最近更新的数据条目
    #     """
    #     raise NotImplementedError("Should implement get_latest_bar()")

    @abstractmethod
    def get_latest_bars(self, symbol, N=1):
        """
        返回最近的N条数据
        """
        raise NotImplementedError("Should implement get_latest_bars()")

    @abstractmethod
    def get_latest_bar_datetime(self, symbol):
        """
        返回最近数据条目对应的Python datetime对象
        """
        raise NotImplementedError("Should implement get_latest_bar_datetime()")

    @abstractmethod
    def get_latest_bar_value(self, symbol, val_type):
        """
        返回最近的数据条目中的Open,High,Low,Close,Volume或者oi的数据
        """
        raise NotImplementedError("Should implement get_latest_bar_value()")

    @abstractmethod
    def get_latest_bars_values(self, symbol, val_type, N=1):
        """
        返回最近的N条数据中的相关数值，如果没有那么多数据
        则返回N-k条数据
        """
        raise NotImplementedError("Should implement get_latest_bars_values()")

    @abstractmethod
    def update_bars(self):
        """
        将最近的数据条目放入到数据序列中，采用元组的格式
        (datetime,open,high,low,close,volume,open interest)
        """
        raise NotImplementedError("Should implement update_bars()")


class HistoricCSVDataHandler(DataHandler):
    """
    HistoricCSVDataHandler类用来读取请求的代码的CSV文件，这些CSV文件
    存储在磁盘上，提供了一种类似于实际交易的场景的”最近数据“一种概念。
    """

    def __init__(self, events, csv_dir, symbol_list, start_date, end_date=None, data_source='yahoo'):
        """
        初始化数据处理
        :param events: 事件队列，queue.Queue()对象
        :param csv_dir: 数据存放位置
        :param symbol_list: 代码列表
        """
        self.events = events
        self.csv_dir = csv_dir
        self.symbol_list = symbol_list
        self.start_date = start_date
        self.end_date = end_date

        # 初始化行情列表:dict，key=symbol，value=pd.DataFrame(csv)
        self.symbol_data = {}
        # 存放最近一条行情记录
        self.latest_symbol_data = {}
        # 初始化数据未完标识
        self.continue_backtest = True
        # 初始化迭代器字典，key=symbol，value=pd.DataFrame(csv).iterrows()
        self.data_generator = {}
        # 初始化数据源
        self._open_convert_csv_files(data_source)

    def _open_convert_csv_files(self, data_source):
        """
        从数据路径中打开CSV文件，将它们转化为pandas的DataFrame。
        这里假设数据来自于yahoo。
        """
        if data_source == 'datayes':
            columns = ['serialNo', 'secID', 'ticker', 'secShortName', 'exchangeCD',
                       'tradeDate', 'preClosePrice', 'actPreClosePrice', 'open',
                       'high', 'low', 'adj_close', 'turnoverVol',
                       'turnoverValue', 'dealAmount', 'turnoverRate', 'accumAdjFactor',
                       'negMarketValue', 'marketValue', 'isOpen', 'vwap']
            index_col = 'tradeDate'
        else:
            columns = ['datetime', 'high', 'low', 'open', 'close', 'volume', 'adj_close']
            index_col = 'datetime'
        # 初始化数据
        for s in self.symbol_list:
            self.symbol_data[s] = pd.read_csv(
                os.path.join(self.csv_dir, '%s.csv' % s),
                header=0, index_col=index_col, parse_dates=True,
                names=columns
            ).sort_index()[:self.end_date]

            if data_source == 'datayes':
                self.symbol_data[s] = self.symbol_data[s][self.symbol_data[s]['isOpen'] == 1]
                self.symbol_data[s]['close'] = self.symbol_data[s]["adj_close"] / self.symbol_data[s]["accumAdjFactor"]
                # pd.DataFrame.pct_change，显示与之前的数差值的百分比
            self.symbol_data[s]["pct_change"] = self.symbol_data[s]["adj_close"].pct_change()
            self.symbol_data[s]["atr"] = talib.ATR(self.symbol_data[s]['high'], self.symbol_data[s]['low'],
                                                   self.symbol_data[s]['adj_close'],
                                                   timeperiod=20)
            # make the symbol_data as a generator
            # 生成可迭代数据
            self.data_generator[s] = self.symbol_data[s].iterrows()
            self.latest_symbol_data[s] = []

    def _get_new_bar(self, symbol):
        """
        从数据集返回最新的数据条目
        """
        for b in self.data_generator[symbol]:
            yield b

    # def get_latest_bar(self, symbol):
    #     """
    #     从最新的symbol_list中返回最新数据条目
    #     """
    #     try:
    #         bars_list = self.latest_symbol_data[symbol]
    #     except KeyError:
    #         print("That symbol is not available in the historical data")
    #         raise
    #     else:
    #         return bars_list[-1]

    def get_latest_bars(self, symbol, N=1):
        """
        从最近的数据列表中获取N条数据，如果没有那么多，则返回N-k条数据
        """
        try:
            bars_list = self.latest_symbol_data[symbol]
        except KeyError:
            print("That symbol is not available in the historical data")
            raise
        else:
            return bars_list[-N:]

    def get_latest_bar_datetime(self, symbol):
        """
        返回最近的数据条目对应的Python datetime
        """
        try:
            bars_list = self.latest_symbol_data[symbol]
        except KeyError:
            print("That symbol is not available in the historical data")
            raise
        else:
            if bars_list:
                return bars_list[-1][0].to_pydatetime()
            else:
                return None

    def get_latest_bar_value(self, symbol, val_type):
        """
        返回最近的数据pandas Series对象中的Open,High,Low,Close,Volume或OI的值
        """
        try:
            bars_list = self.latest_symbol_data[symbol]
        except KeyError:
            print("That Symbol is not available in the historical data")
            raise
        else:
            if bars_list:
                return getattr(bars_list[-1][1], val_type)
            else:
                return 0

    def get_latest_bars_values(self, symbol, val_type, N=1):
        """
        返回latest_symbol_list中的最近N条数据，如果没有那么多，返回N-k条
        """
        try:
            bars_list = self.get_latest_bars(symbol, N)
        except KeyError:
            print("That Symbol is not available in the historical data")
            raise
        else:
            return np.array([getattr(b[1], val_type) for b in bars_list])

    def update_bars(self):
        """
        将最近的数据条目放入到latest_symbol_data结构中。
        """
        for s in self.symbol_list:
            try:
                bar = next(self._get_new_bar(s))
            except StopIteration:
                self.continue_backtest = False
            else:
                if bar is not None:
                    self.latest_symbol_data[s].append(bar)
        self.events.put(MarketEvent())
