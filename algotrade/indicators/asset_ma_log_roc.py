import backtrader as bt


class AssetMALogROC(bt.Indicator):
    """
    Formula:
        - asset_ma_log_roc = log(asset / ma_period(asset)) = log(asset) - log(ma_period(asset))
    """

    lines = ('values',)

    params = (
        ('period', 12),
        ('movav', bt.indicators.MovAv.SMA),
        ('csv', False)
    )

    def __init__(self):
        self.l.values = bt.talib.LN(self.data) - bt.talib.LN(self.p.movav(self.data, period=self.p.period))
        super().__init__()
        self.csv = self.p.csv
