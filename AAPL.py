# -*- coding: utf-8 -*-

# mac.py

import datetime
import math
import os
from event import OrderEvent
from backtest import Backtest
from data import HistoricCSVDataHandler
from execution import SimulatedExecutionHandler
from portfolio import Portfolio
from Strategies.MovingAverageCrossStrategy import MovingAverageCrossStrategy


# Tasks to do:
# 1. Complete the sea turtle strategy
# 2. Multiple strategies
# 3. Run every day automatically
# 4. Send text when one of the strategy find something


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
        mkt_quantity = math.floor(all_in_cash / order_price / 100) * 100
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


if __name__ == "__main__":
    # 初始化待处理数据的路径，支持对多个行情文件进行批量处理，行情文件命名与symbol_list内一致
    path1 = os.path.abspath('.')
    csv_dir = 'data_csv'
    csv_dir = os.path.join(path1, csv_dir)
    symbol_list = ['002230']
    data_source = 'datayes'
    # symbol_list = ['AAPL']
    # data_source = 'yahoo'
    # 初始化初始资金
    initial_capital = 100000.0

    # todo 未知用途
    heartbeat = 0.0

    # 初始化回测开始时间
    start_date = datetime.datetime(2010, 5, 1, 0, 0, 0)
    end_date = datetime.datetime(2015, 5, 1, 0, 0, 0)

    # 执行回测
    backtest = Backtest(
        csv_dir, symbol_list, data_source, initial_capital, heartbeat,
        data_handler_cls=HistoricCSVDataHandler, execution_handler_cls=SimulatedExecutionHandler,
        portfolio_cls=My_portfolio, strategy_cls=MovingAverageCrossStrategy, start_date=start_date, end_date=end_date
    )
    backtest.run_trading()
