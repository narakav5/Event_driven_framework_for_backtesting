# -*- coding: utf-8 -*-
#
# backtest.py


import pprint
import queue
import time
from BackTest.equity_plot import plot_performance
import pandas as pd


class Backtest(object):
    """
    Back_test class. The main class that capsule every thing
    """

    def __init__(
            self, csv_dir, symbol_list, data_source, initial_capital,
            heartbeat, data_handler_cls,
            execution_handler_cls, portfolio_cls, strategy_cls, start_date, end_date=None
    ):
        """
        初始化回测单元
        :param csv_dir: 存放csv的路径
        :param symbol_list: 股票代码列表，用于关联csv路径下的文件，并作为传递字典对象的keys
        :param initial_capital: 初始资金
        :param heartbeat: 未知
        :param start_date: 回测开始时间
        :param data_handler_cls: 数据处理类
        :param execution_handler_cls: 执行处理类
        :param portfolio_cls: 交易逻辑类
        :param strategy_cls: 量化策略类
        """
        # 初始化创建对象输入的参数
        self.csv_dir = csv_dir
        self.symbol_list = symbol_list
        self.data_source = data_source
        self.initial_capital = initial_capital

        self.heartbeat = heartbeat
        self.start_date = start_date
        self.end_date = end_date

        self.data_handler_cls = data_handler_cls
        self.execution_handler_cls = execution_handler_cls
        self.portfolio_cls = portfolio_cls
        self.strategy_cls = strategy_cls

        # 初始化队列对象
        self.events = queue.Queue()

        # todo 未知用途
        self.signals = 0
        self.orders = 0
        self.fills = 0

        # 初始化生成与交易关联的所有实例
        self._generate_trading_instances()

        # self.strat_params_list=strat_params_list

    def _generate_trading_instances(self):
        """
        Generate all the instances associated with the trading: data handler, strategy  and execution_handler instance
        生成与交易关联的所有实例：数据处理程序、策略和执行处理程序实例
        """
        print(
            "Creating DataHandler,Strategy,Portfolio and ExecutionHandler/n"
        )
        self.data_handler = self.data_handler_cls(self.events, self.csv_dir,
                                                  self.symbol_list, self.start_date, self.end_date, self.data_source)
        self.strategy = self.strategy_cls(
            self.data_handler,
            self.events)
        self.portfolio = self.portfolio_cls(self.data_handler, self.events, self.start_date,
                                            self.initial_capital)  # create instance of portfolio
        self.execution_handler = self.execution_handler_cls(self.events, self.symbol_list)

    def _run_backtest(self):
        """
        执行回测
        """
        i = 0
        while True:
            i += 1
            print(i)
            if self.data_handler.continue_backtest:
                self.data_handler.update_bars()  # Trigger a market event
            else:
                break
            while True:
                try:
                    # Get an event from the Queue
                    event = self.events.get(False)
                    print("event.type:{}".format(event.type))
                except queue.Empty:
                    break
                else:
                    if event is not None:
                        if event.type == 'MARKET':
                            self.strategy.calculate_signals(
                                event)  # Trigger a Signal event #
                            self.portfolio.update_timeindex()
                        # elif event.type == 'SIGNAL':
                        elif event.type == 'SIGNAL' and event.datetime >= self.start_date:
                            self.signals += 1
                            self.portfolio.update_signal(
                                event)  # Transfer Signal Event to order Event and trigger an order event
                        elif event.type == 'ORDER':
                            self.orders += 1
                            self.execution_handler.execute_order(event)
                        # finish the order by updating the position. This is
                        # quite naive, further extention is required.
                        elif event.type == 'FILL':
                            self.fills += 1
                            self.portfolio.update_fill(event)

            time.sleep(self.heartbeat)

    def _output_performance(self):

        self.portfolio.create_equity_curve_dateframe()  # get equity curve object

        print("Creating summary stats...")
        stats = self.portfolio.output_summary_stats()

        print("Creating equity curve...")
        print(self.portfolio.equity_curve.tail(10))
        pprint.pprint(stats)

        print("Signals: %s" % self.signals)
        print("Orders: %s" % self.orders)
        print("Fills: %s" % self.fills)
        self.portfolio.equity_curve.round(2).to_csv('.\\output\\equity.csv')
        # self.execution_handler.execution_records.set_index('date_time',inplace =True)
        self.execution_handler.execution_records.round(2).to_csv(
            '.\\output\\Execution_summary.csv')

    def run_trading(self):
        """
        模拟回测以及输出业绩结果的过程
        """
        self._run_backtest()
        self._output_performance()
        symbol_data = pd.DataFrame()
        for symbol in self.symbol_list:
            symbol_data = symbol_data.append(self.data_handler.symbol_data[symbol])
        symbol_data = symbol_data.set_index('ticker', append=True, drop=False).swaplevel()
        my_plot = plot_performance(self.portfolio.equity_curve.round(2),
                                   symbol_data,
                                   self.execution_handler.execution_records)
        my_plot.plot_equity_curve()
        my_plot.plot_stock_curve()
        my_plot.show_all_plot()
        # out=open("opt.csv","w")
        # spl=len(self.strat_params_list)
        # for i,sp in enumerate(self.strat_params_list):
        #     print("Strategy %s out of %s..." %(i+1,spl))
        #     self._generate_trading_instances(sp)
        #     self._run_backtest()
        #     stats=self._output_performance()
        #     pprint.pprint(stats)
        #
        #     tot_ret=float(stats[0][1].replace("%",""))
        #     sharpe=float(stats[1][1])
        #     max_dd=float(stats[2][1].replace("%",""))
        #     dd_dur=int(stats[3][1])
        #
        #     out.write(
        #         "%s,%s,%s,%s,%s,%s,%s\n" %
        #         sp["ols_window"],sp["zscore_high"],sp["zscore_low"],
        #         tot_ret,sharpe,max_dd,dd_dur
        #     )
        # out.close()
