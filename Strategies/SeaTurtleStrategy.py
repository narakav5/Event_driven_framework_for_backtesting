import numpy as np
import datetime
from Events.SignalEvent import SignalEvent
from Strategies.strategy import Strategy


class SeaTurtleStrategy(Strategy):
    """
    用来进行基本的移动平均跨越测录的实现，这个策略有一组短期和长期的简单移动平均值。
    默认的短期/长期的窗口分别是100天和400天。
    """

    def __init__(self, bars, events,long_window=20):
        # data_handler
        self.bars = bars
        self.symbol_list = self.bars.symbol_list
        self.events = events
        # 初始化止损价
        self.stop_loss = 0
        # 用于计算突破的短期和长期窗口
        self.long_window = long_window
        # 初始化上一次信号标识
        self.bought = self._calculate_initial_bought()

    def _calculate_initial_bought(self):
        """
        给bought字典增加键，对于所有的代码都设置值为OUT
        """
        bought = {}
        for s in self.symbol_list:
            bought[s] = 'OUT'
        return bought

    def calculate_signals(self, event):
        """
        基于MAC SMA生成一组新的信号，进入市场的标志就是短期的移动平均超过
        长期的移动平均。
        """
        if event.type == 'MARKET':
            for s in self.symbol_list:
                adj_close_prices = self.bars.get_latest_bars_values(s, "adj_close", N=self.long_window)
                high_prices=self.bars.get_latest_bars_values(s, "high", N=self.long_window)
                low_prices = self.bars.get_latest_bars_values(s, "low", N=self.long_window)
                bar_date = self.bars.get_latest_bar_datetime(s)
                if adj_close_prices is not None and adj_close_prices != []:
                    if len(adj_close_prices) >= self.long_window:
                        don_open = np.max(adj_close_prices[-self.long_window:])
                        don_close = np.min(adj_close_prices[-self.long_window:])
                        symbol = s
                        dt = datetime.datetime.utcnow()
                        last_close_price = self.bars.get_latest_bar_value(s, 'adj_close')
                        print("don_open:{},close_pirce:{}".format(don_open, last_close_price))
                        last_atr = self.bars.get_latest_bar_value(s, 'atr')
                        if last_close_price >= don_open and self.bought[s] == "OUT":
                            print("LONG: %s" % bar_date)
                            sig_dir = 'LONG'
                            signal = SignalEvent(1, bar_date, symbol, dt, sig_dir, last_close_price, 1.0)
                            self.events.put(signal)
                            self.stop_loss = last_close_price - 2*last_atr
                            self.bought[s] = 'LONG'
                        elif last_close_price <= self.stop_loss and self.bought[s] == "LONG":
                            print("SHORT:%s" % bar_date)
                            sig_dir = 'STOP_LOSS'
                            signal = SignalEvent(1, bar_date, symbol, dt, sig_dir, last_close_price, 1.0)
                            self.events.put(signal)
                            self.bought[s] = 'OUT'
                        elif last_close_price <= don_close and self.bought[s] == "LONG":
                            print("SHORT:%s" % bar_date)
                            sig_dir = 'EXIT'
                            signal = SignalEvent(1, bar_date, symbol, dt, sig_dir, last_close_price, 1.0)
                            self.events.put(signal)
                            self.bought[s] = 'OUT'
