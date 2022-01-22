# -*- coding: utf-8 -*-

# plot_performance.py

import os.path

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import mplfinance as mpl
from mplfinance.original_flavor import candlestick_ohlc
import matplotlib.dates as mdates
from matplotlib.dates import date2num
import copy
import pandas as pd


class plot_performance():
    def __init__(self, equity_curve, stock_curve, summary_recording):
        self.equity_data = equity_curve
        self.stock_data = stock_curve
        self.summary_recording = summary_recording.copy(deep=True)
        self.summary_recording = self.summary_recording.set_index(['symbol', 'date_time'], drop=False)
        print(self.summary_recording)
        close_price = self.stock_data.loc[self.summary_recording.index, :]['adj_close']
        self.summary_recording['close_price'] = close_price
        self.fig = plt.figure()
        self.fig.patch.set_facecolor('white')

    def plot_equity_curve(self):
        ax1 = self.fig.add_subplot(111, ylabel='Portfolio value: %')
        self.equity_data['equity_curve'].plot(ax=ax1, color='red', lw=2.)
        plt.grid(True)
        plt.show()

    def plot_stock_curve(self):
        for symbol in self.stock_data.index.levels[0]:
            self.fig = plt.figure()
            # self.fig.patch.set_facecolor('white')
            ax2 = self.fig.add_subplot(111, ylabel='Stock value: %')
            # self.stock_data['adj_close'].plot(ax=ax2, color='blue', lw=2.)
            ohlc = self.stock_data.loc[symbol][['open', 'high', 'low', 'adj_close']]
            ohlc = ohlc.reset_index().values
            date = date2num(ohlc[:, 0])
            ohlc[:, 0] = date
            # tem_date_num = date2num(le['date_time'])
            # le.loc[:,'date_time'] = tem_date_num
            le_y = self.summary_recording.loc[symbol][self.summary_recording.loc[symbol]['direction'] == 'LONG'][
                'close_price']
            le_x = self.summary_recording.loc[symbol][
                self.summary_recording.loc[symbol]['direction'] == 'LONG'].index.to_list()
            le_x_value = date2num(le_x)
            le_y_value = le_y.values

            lexit_y = self.summary_recording.loc[symbol][self.summary_recording.loc[symbol]['direction'] == 'EXIT'][
                'close_price']
            lexit_x = self.summary_recording.loc[symbol][
                self.summary_recording.loc[symbol]['direction'] == 'EXIT'].index.to_list()
            lexit_x_value = date2num(lexit_x)
            lexit_y_value = lexit_y.values
            # mpl.plot(ax2, ohlc, width=0.4, colorup='red', colordown='green')
            candlestick_ohlc(ax2, ohlc, width=0.4, colorup='red', colordown='green')
            for label in ax2.xaxis.get_ticklabels():
                label.set_rotation(45)
            ax2.plot(le_x_value, le_y_value, '^', color='lime', markersize=8,
                     label='long enter')
            for index in range(len(le_x_value)):
                plt.text(le_x_value[index], le_y_value[index] * 1.05, "Buy", ha='center', va='bottom', fontsize=8)

            ax2.plot(lexit_x_value, lexit_y_value, 'v', color='red', markersize=8,
                     label='Exit')
            for index in range(len(lexit_x_value)):
                plt.text(lexit_x_value[index], lexit_y_value[index] * 1.05, "Sell", ha='center', va='bottom',
                         fontsize=8)

            ax2.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
            ax2.xaxis.set_major_locator(mticker.MaxNLocator(10))
            plt.title = symbol
            plt.grid(True)
            plt.show()

    def show_all_plot(self):
        pass
        # plt.show()
# if __name__=="__main__":
#     data=pd.io.parsers.read_csv(
#         "equity.csv",header=0,
#         parse_dates=True,index_col=0
#     ).sort_index()
#     fig=plt.figure()
#     fig.patch.set_facecolor('white')
#
#     ax1=fig.add_subplot(311,ylabel='Portfolio value: %')
#     data['equity_curve'].plot(ax=ax1,color='blue',lw=2.)
#     plt.grid(True)
#
#     ax2=fig.add_subplot(312,ylabel='Period returns,%')
#     data['returns'].plot(ax=ax2,color='black',lw=2.)
#     plt.grid(True)
#
#     ax3=fig.add_subplot(313,ylabel='Drawdowns, %')
#     data['drawdown'].plot(ax=ax3,color='red',lw=2.)
#     plt.grid(True)
#
#     plt.show()
