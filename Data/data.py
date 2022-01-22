# -*- coding: utf-8 -*-

# data.py

from abc import ABCMeta, abstractmethod
import os
import os.path

import numpy as np
import pandas as pd
import talib

from Events.MarketEvent import MarketEvent


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



