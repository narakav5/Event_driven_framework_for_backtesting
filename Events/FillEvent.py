from .event import Event


class FillEvent(Event):
    """
    封装订单执行这样一种概念，这个概念是由交易所所返回的。存储交易的数量，
    价格。另外，还要存储交易的佣金和手续费。
    在这里不支持一个订单有多个价格。
    """

    def __init__(self, date_time, symbol, quantity, buy_or_sell,
                 order_price, commission=None):
        self.type = 'FILL'
        self.date_time = date_time
        self.symbol = symbol
        # self.exchange = exchange
        self.quantity = quantity
        self.buy_or_sell = buy_or_sell
        self.order_price = order_price

        if commission is None:
            self.commission = self.calculate_ib_commission()
        else:
            self.commission = commission

    def calculate_ib_commission(self):
        """
        用来计算基于Interactive Brokers的交易费用。
        """
        stamp_tax = 0.001  # 卖
        transaction_fees = 0.0000687  # 买卖
        transfer_fees = 0.0002  # 买卖
        brokerage = 0.003  # 买卖
        if self.buy_or_sell == "BUY":
            full_cost = self.order_price * self.quantity * (transaction_fees + transfer_fees + brokerage)
        elif self.buy_or_sell == "SELL":
            full_cost = self.order_price * self.quantity * (stamp_tax + transaction_fees + transfer_fees + brokerage)
        else:
            raise ValueError("未输入交易信号")
        print(full_cost)
        return full_cost
