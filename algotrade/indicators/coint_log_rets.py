import numpy as np
import backtrader as bt
from .log_ret import LogReturn


class CointLogRets(bt.Indicator):
    """
    Formula:
        x = log_ret0 = log(data0) - log(data0(-period0))
        y = log_ret1 = log(data1) - log(data1(-period1))

        - values = coint(log_ret0, log_ret1, period)
    """

    _mindatas = 2

    lines = ('values',)

    params = (
        ('period0', 1),
        ('period1', 1),
        ('period', 30),
        ('csv', False)
    )

    def __init__(self):
        coint = bt.indicators.CointN(
            LogReturn(self.data0, period=self.p.period0).values,
            LogReturn(self.data1, period=self.p.period1).values,
            period=self.p.period
        )

        self.l.values = coint.pvalue

        super().__init__()
        self.csv = self.p.csv
