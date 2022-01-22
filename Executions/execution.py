# -*- coding: utf-8 -*-

# execution.py

from __future__ import print_function

from abc import ABCMeta, abstractmethod

try:
    import Queue as queue
except ImportError:
    import queue


class ExecutionHandler(object, metaclass=ABCMeta):
    """
    ExecutionHandler抽象类处理由Portfolio生成的order对象与实际市场中发生的
    Fill对象之间的交互。
    这个类可以用于实际的成交，或者模拟的成交
    """

    @abstractmethod
    def execute_order(self, event):
        """
        获取一个Order事件并执行，产生Fill事件放到事件队列中
        """
        raise NotImplementedError("Should implement execute_order()")
