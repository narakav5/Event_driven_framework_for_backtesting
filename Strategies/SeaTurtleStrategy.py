from Strategies.strategy import Strategy
import numpy as np
import datetime
from event import SignalEvent
from Strategies import MovingAverageCrossStrategy


class SeaTurtleStrategy(MovingAverageCrossStrategy):
    """
    用来进行基本的移动平均跨越测录的实现，这个策略有一组短期和长期的简单移动平均值。
    默认的短期/长期的窗口分别是100天和400天。
    """

    def __init__(self, long_window=20):
        # 初始化止损价
        self.stop_loss = self._calculate_initial_stop_loss()
        # 用于计算突破的短期和长期窗口
        self.long_window = long_window

    def _calculate_initial_stop_loss(self):
        """
        给stop_loss字典增加键，对于所有的代码都设置值为0
        """
        stop_loss = {}
        for s in self.symbol_list:
            stop_loss[s] = 0
        return stop_loss

    def calculate_signals(self, event):
        """
        基于MAC SMA生成一组新的信号，进入市场的标志就是短期的移动平均超过
        长期的移动平均。
        """
        if event.type == 'MARKET':
            for s in self.symbol_list:
                adj_close_prices = self.bars.get_latest_bars_values(s, "adj_close", N=self.long_window)
                bar_date = self.bars.get_latest_bar_datetime(s)

                if adj_close_prices is not None and adj_close_prices != []:
                    if len(adj_close_prices) >= self.long_window:
                        long_sma = np.mean(adj_close_prices[-self.long_window:])
                        symbol = s
                        dt = datetime.datetime.utcnow()
                        last_close_price = self.bars.get_latest_bar_value(s, 'adj_close')
                        if last_close_price > long_sma and self.bought[s] == "OUT":
                            print("LONG: %s" % bar_date)
                            sig_dir = 'LONG'
                            signal = SignalEvent(1, bar_date, symbol, dt, sig_dir, last_close_price, 1.0)
                            self.events.put(signal)
                            self.bought[s] = 'LONG'
                        elif last_close_price < long_sma and self.bought[s] == "LONG":
                            print("SHORT:%s" % bar_date)
                            sig_dir = 'EXIT'
                            signal = SignalEvent(1, bar_date, symbol, dt, sig_dir, last_close_price, 1.0)
                            self.events.put(signal)
                            self.bought[s] = 'OUT'
