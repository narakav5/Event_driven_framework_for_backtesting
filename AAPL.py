# -*- coding: utf-8 -*-

# mac.py

import datetime
import os
from BackTest.backtest import Backtest
from Data.HistoricCSVDataHandler import HistoricStockCSVDataHandler
from Executions.SimulatedExecutionHandler import SimulatedExecutionHandler
from Strategies.SeaTurtleStrategy import SeaTurtleStrategy
from Portfolios.SingleSymbolPortfolio import My_portfolio

# Tasks to do:
# 1. Complete the sea turtle strategy
# 2. Multiple strategies
# 3. Run every day automatically
# 4. Send text when one of the strategy find something


if __name__ == "__main__":
    # 初始化待处理数据的路径，支持对多个行情文件进行批量处理，行情文件命名与symbol_list内一致
    path1 = os.path.abspath('.')
    csv_dir = 'data_csv'
    csv_dir = os.path.join(path1, csv_dir)
    symbol_list = ['600036', '600639']
    data_source = 'datayes'
    # symbol_list = ['AAPL']
    # data_source = 'yahoo'
    # 初始化初始资金
    initial_capital = 100000.0

    # todo 未知用途
    heartbeat = 0.0

    # 初始化回测开始时间
    start_date = datetime.datetime(2015, 1, 1, 0, 0, 0)
    end_date = datetime.datetime(2021, 12, 31, 0, 0, 0)

    # 执行回测
    backtest = Backtest(
        csv_dir, symbol_list, data_source, initial_capital, heartbeat,
        data_handler_cls=HistoricStockCSVDataHandler, execution_handler_cls=SimulatedExecutionHandler,
        portfolio_cls=My_portfolio, strategy_cls=SeaTurtleStrategy, start_date=start_date, end_date=end_date
    )
    backtest.run_trading()
