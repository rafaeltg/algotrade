import backtrader as bt


class AssetMADiff(bt.Indicator):
    """
    Formula:
        - asset_ma_diff = asset - ma_period(asset)
    """

    lines = ('values',)

    params = (
        ('period', 12),
        ('movav', bt.indicators.MovAv.SMA),
        ('csv', False)
    )

    def __init__(self):
        self.l.values = self.data - self.p.movav(self.data, period=self.p.period)
        super().__init__()
        self.csv = self.p.csv
