import backtrader as bt


class MAsDiff(bt.Indicator):
    """
    Formula:
        - mas_diff = ma_fast(data) - ma_slow(data)
    """

    lines = ('values',)

    params = (
        ('fast_period', 9),
        ('fast_movav', bt.indicators.MovAv.SMA),
        ('slow_period', 20),
        ('slow_movav', bt.indicators.MovAv.SMA),
        ('csv', False)
    )

    def __init__(self):
        self.l.values = self.p.fast_movav(self.data, period=self.p.fast_period) - \
                        self.p.slow_movav(self.data, period=self.p.slow_period)

        super().__init__()
        self.csv = self.p.csv
