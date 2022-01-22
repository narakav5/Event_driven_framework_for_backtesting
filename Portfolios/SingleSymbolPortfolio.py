from .portfolio import Portfolio
import math
from Events.OrderEvent import OrderEvent


# 我的投资组合
class My_portfolio(Portfolio):
    # 生成原始订单
    def generate_naive_order(self, signal):
        """

        :param signal: event.SignalEvent()
        :return: event.OrderEvent()
        """
        order = None
        date_time = signal.date_time
        symbol = signal.symbol
        direction = signal.signal_type
        order_price = signal.order_price
        all_in_cash = self.current_holdings['cash']
        # mkt_quantity = math.floor(all_in_cash / order_price / 100) * 100
        mkt_quantity = 100
        cur_quantity = self.current_positions[symbol]
        order_type = 'MKT'

        if direction == 'LONG' and cur_quantity == 0:
            order = OrderEvent(
                date_time,
                symbol,
                order_type,
                mkt_quantity,
                'BUY',
                order_price,
                direction)
        if direction == 'SHORT' and cur_quantity == 0:
            order = OrderEvent(
                date_time,
                symbol,
                order_type,
                mkt_quantity,
                'SELL',
                order_price,
                direction)
        if direction == 'EXIT' and cur_quantity > 0:
            order = OrderEvent(
                date_time,
                symbol,
                order_type,
                abs(cur_quantity),
                'SELL',
                order_price,
                direction)
        if direction == 'STOP_LOSS' and cur_quantity > 0:
            order = OrderEvent(
                date_time,
                symbol,
                order_type,
                abs(cur_quantity),
                'SELL',
                order_price,
                direction)
        if direction == 'EXIT' and cur_quantity < 0:
            order = OrderEvent(
                date_time,
                symbol,
                order_type,
                abs(cur_quantity),
                'BUY',
                order_price,
                direction)

        return order
