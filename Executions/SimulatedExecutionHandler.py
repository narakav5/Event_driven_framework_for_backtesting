from .execution import ExecutionHandler
import pandas as pd
from Events.FillEvent import FillEvent


class SimulatedExecutionHandler(ExecutionHandler):
    """
    这是一个模拟的执行处理，简单的将所有的订单对象转化为等价的成交对象，不考虑
    时延，滑价以及成交比率的影响。
    """

    def __init__(self, events, symbol_list):
        self.events = events
        self.execution_records = pd.DataFrame(columns=['date_time', 'symbol', 'direction', 'quantity', 'order_price',
                                                       'return_profit', 'return_profit_pct'])
        self.symbol_list = symbol_list
        self.recent_deal_average_cost = self.__init_recent_deal_average_cost()
        self.entry_time = 0

    def __init_recent_deal_average_cost(self):
        __d = {}
        for symbol in self.symbol_list:
            __d[symbol] = 0
        return __d

    def execute_order(self, event):
        """
        Generate the order event and make the execution log
        """
        if event.type == 'ORDER':
            fill_event = FillEvent(event.date_time,
                                   event.symbol,
                                   event.quantity, event.buy_or_sell, order_price=event.order_price, commission=None)
            self.events.put(fill_event)
            if event.direction != 'EXIT':
                self.entry_time += 1
                self.execution_records = self.execution_records.append(
                    pd.DataFrame(
                        {'date_time': [event.date_time], 'symbol': [event.symbol], 'direction': [event.direction],
                         'quantity': [event.quantity], 'order_price': [event.order_price],
                         'return_profit': None, 'return_profit_pct': None}))
                self.recent_deal_average_cost[event.symbol] = self.recent_deal_average_cost[event.symbol] * (
                    self.entry_time - 1) / (
                    self.entry_time) + (
                    event.order_price / self.entry_time)
            else:
                return_profit = (
                    event.order_price - self.recent_deal_average_cost[event.symbol]) * event.quantity
                return_profit_pct = (event.order_price - self.recent_deal_average_cost[event.symbol]) / \
                    self.recent_deal_average_cost[event.symbol]
                self.execution_records = self.execution_records.append(
                    pd.DataFrame(
                        {'date_time': [event.date_time], 'symbol': [event.symbol], 'direction': [event.direction],
                         'quantity': [event.quantity], 'order_price': [event.order_price],
                         'return_profit': return_profit,
                         'return_profit_pct': return_profit_pct}))
                self.recent_deal_average_cost[event.symbol] = 0
                self.entry_time = 0
