from .event import Event

class SignalEvent(Event):
    """
    处理从Strategy对象发来的信号的事件，信号会被Portfolio对象所接收并且
    根据这个信号来采取行动
    """

    def __init__(self, strategy_id, date_time, symbol, datetime, signal_type, order_price, strength, stop_loss=None):
        self.strategy_id = strategy_id
        self.date_time = date_time
        self.type = 'SIGNAL'
        self.symbol = symbol
        self.datetime = datetime
        self.signal_type = signal_type
        self.strength = strength
        self.order_price = order_price
        self.stop_loss = stop_loss
