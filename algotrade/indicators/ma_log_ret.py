import backtrader as bt
from .log_ret import LogReturn


class MALogReturn(LogReturn):
    """
    Formula:
        - values = log(movav(data, movav_period)) - log(movav(data, movav_period)(-period)))
    """

    params = (
        ('movav_period', 12),
        ('movav', bt.indicators.MovAv.SMA),
    )

    def __init__(self):
        self.data = self.p.movav(self.data, period=self.p.movav_period)
        super().__init__()
