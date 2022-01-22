from .event import Event


class MarketEvent(Event):
    """
    处理接收到新的市场数据的更新
    """

    def __init__(self):
        self.type = 'MARKET'