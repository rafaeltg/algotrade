import backtrader as bt
from .log_ret import LogReturn


class CorrelLogReturns(bt.talib.CORREL):
    """
    Formula:
        x = log_ret0 = log(data0) - log(data0(-period0))
        y = log_ret1 = log(data1) - log(data1(-period1))

        - real = corr(log_ret0, log_ret1, period)
    """

    params = (
        ('period0', 1),
        ('period1', 1),
        ('csv', False)
    )

    def __init__(self):
        self.data0 = LogReturn(self.data0, period=self.p.period0).values
        self.data1 = LogReturn(self.data1, period=self.p.period1).values
        super().__init__()
        self.csv = self.p.csv
