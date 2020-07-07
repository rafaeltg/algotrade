import backtrader as bt


class LogReturn(bt.Indicator):
    """
    Logarithmic return

    Formula:
        - log_ret = log(data / data_period) = log(data) - log(data_period)
    """

    lines = ('values',)

    params = (
        ('period', 12),
        ('csv', False),
    )

    def __init__(self):
        self.l.values = bt.talib.LN(self.data) - bt.talib.LN(self.data(-self.p.period))
        super().__init__()
        self.csv = self.p.csv
