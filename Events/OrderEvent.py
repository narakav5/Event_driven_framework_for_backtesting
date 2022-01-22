from .event import Event


class OrderEvent(Event):
    """
    处理向执行系统提交的订单（Order）信息。这个订单包括一个代码，一个类型
    （市价还是限价），数量以及方向
    """

    def __init__(self, date_time, symbol, order_type, quantity, buy_or_sell, order_price, direction):
        self.date_time = date_time
        self.type = 'ORDER'
        self.symbol = symbol
        self.order_type = order_type
        self.quantity = quantity
        self.buy_or_sell = buy_or_sell
        self.direction = direction
        self.order_price = order_price

    def print_order(self):
        """
        输出订单中的相关信息
        """
        print(
            "Order:Symbol:%s,Type=%s,Quantity=%s,Direction=%s, Order_price=%s" %
            (self.symbol, self.order_type, self.quantity, self.direction, self.order_price)
        )