import numpy as np
import backtrader as bt


class ZigZag(bt.ind.PeriodN):
    """
    Identifies Peaks/Troughs of a timeseries
    """

    lines = (
        'zigzag_peak',
        'zigzag_valley',
        'zigzag'
    )

    plotinfo = dict(
        subplot=False,
        plotlinelabels=True,
        plotlinevalues=True,
        plotvaluetags=True,
    )

    plotlines = dict(
        zigzag_peak=dict(marker='v', markersize=4.5, color='red', fillstyle='full', ls=''),
        zigzag_valley=dict(marker='^', markersize=4.5, color='black', fillstyle='full', ls=''),
        zigzag=dict(_name='zigzag', color='darkblue', ls='-', _skipnan=True),
    )

    params = (
        ('period', 2),
        ('up_retrace', 0.1),
        ('down_retrace', 0.1),
        ('bardist', 0.015),  # distance to max/min in absolute perc (for plotting)
    )

    def __init__(self):
        super(ZigZag, self).__init__()

        if not self.p.up_retrace:
            raise ValueError('Upward retracement should not be zero.')

        if not self.p.down_retrace:
            raise ValueError('Downward retracement should not be zero.')

        if self.p.up_retrace < 0:
            self.p.up_retrace = -self.p.up_retrace

        if self.p.down_retrace > 0:
            self.p.down_retrace = -self.p.down_retrace

        self._trend = 0
        self._last_pivot_t = 0
        self._last_pivot_x = 0
        self._last_pivot_ago = 0

    def prenext(self):
        self._trend = 0
        self._last_pivot_t = 0
        self._last_pivot_x = self.data[0]
        self._last_pivot_ago = 0

        self.lines.zigzag_peak[0] = np.NaN
        self.lines.zigzag_valley[0] = np.NaN
        self.lines.zigzag[0] = np.NaN

    def next(self):
        data = self.data
        zigzag_peak = self.lines.zigzag_peak
        zigzag_valley = self.lines.zigzag_valley
        zigzag = self.lines.zigzag

        x = data[0]
        r = x / self._last_pivot_x - 1
        curr_idx = len(data) - 1

        self._last_pivot_ago = curr_idx - self._last_pivot_t
        zigzag_peak[0] = np.NaN
        zigzag_valley[0] = np.NaN
        zigzag[0] = np.NaN

        if self._trend == 0:
            if r >= self.p.up_retrace:
                zigzag_valley[-int(self._last_pivot_ago)] = self._last_pivot_x * (1 - self.p.bardist)
                zigzag[-int(self._last_pivot_ago)] = self._last_pivot_x
                self._trend = 1
                self._last_pivot_x = x
                self._last_pivot_t = curr_idx
            elif r <= self.p.down_retrace:
                zigzag_peak[-int(self._last_pivot_ago)] = self._last_pivot_x * (1 + self.p.bardist)
                zigzag[-int(self._last_pivot_ago)] = self._last_pivot_x
                self._trend = -1
                self._last_pivot_x = x
                self._last_pivot_t = curr_idx

        elif self._trend == -1:
            if r >= self.p.up_retrace:
                zigzag_valley[-int(self._last_pivot_ago)] = self._last_pivot_x * (1 - self.p.bardist)
                zigzag[-int(self._last_pivot_ago)] = self._last_pivot_x
                self._trend = 1
                self._last_pivot_x = x
                self._last_pivot_t = curr_idx
            elif x < self._last_pivot_x:
                self._last_pivot_x = x
                self._last_pivot_t = curr_idx

        elif self._trend == 1:
            if r <= self.p.down_retrace:
                zigzag_peak[-int(self._last_pivot_ago)] = self._last_pivot_x * (1 + self.p.bardist)
                zigzag[-int(self._last_pivot_ago)] = self._last_pivot_x
                self._trend = -1
                self._last_pivot_x = x
                self._last_pivot_t = curr_idx
            elif x > self._last_pivot_x:
                self._last_pivot_x = x
                self._last_pivot_t = curr_idx
