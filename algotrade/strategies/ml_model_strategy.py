import numpy as np
import backtrader as bt
from ..indicators import *
from pydl.scripts import optimization, get_search_space


class Y(bt.Indicator):
    """
        peak    = -1 = sell
        neutral =  0 = do nothing
        valley  =  1 = buy
    """

    lines = ('y',)
    params = (
        ('period', 1),
        ('csv', False)
    )

    def __init__(self):
        super().__init__()
        self._zz = ZigZag(self.data, up_retrace=0.05, down_retrace=-0.05)
        self.csv = self.p.csv

    def prenext(self):
        if not np.isnan(self._zz.zigzag_valley[0]):
            self.l.y[0] = 1
        elif not np.isnan(self._zz.zigzag_peak[0]):
            self.l.y[0] = -1
        else:
            self.l.y[0] = 0

    def next(self):
        if not np.isnan(self._zz.zigzag_valley[0]):
            self.l.y[0] = 1
        elif not np.isnan(self._zz.zigzag_peak[0]):
            self.l.y[0] = -1
        else:
            self.l.y[0] = 0


class MLModelStrategy(bt.Strategy):
    params = dict(
        model_search_space=None,
        stop_loss=0.2,  # price is 2% less than the entry point
        trail=False,
        printout=False,
        csv=False,
    )

    def __init__(self):
        # Set timer to refit model every last trading of week
        self.add_timer(
            when=bt.timer.SESSION_END,
            weekdays=[5],
            weekcarry=True,
        )

        self.order = None
        self._model = None

        self._set_x()
        self.y = Y(self.data.close, csv=self.p.csv)

    def log(self, txt, dt=None):
        if self.p.printout:
            dt = dt or self.data.datetime[0]
            if isinstance(dt, float):
                dt = bt.num2date(dt)
            print('[{}] {}'.format(dt.strftime("%Y-%m-%d %H:%M"), txt))

    def next(self):
        txt = '-- next {}, O {:.2f}, H {:.2f}, L {:.2f}, C {:.2f}'.format(
            len(self),
            self.data.open[0],
            self.data.high[0],
            self.data.low[0],
            self.data.close[0])

        self.log(txt)

        self._get_x()

    def notify_timer(self, timer, when, *args, **kwargs):
        self.log('-- Refitting model - {} - len: {}'.format(when, len(self)))

        x = self._get_x()
        y = np.array(self.y.get(0, len(self)))

        return
        _, self._model = optimization(
            search_space=get_search_space(self.p.model_search_space, features=list(x[0])),
            x=x,
            y=y,
            cmaes_params=dict(
                pop_size=30,
                max_iter=100,
                adapt_sigma=True,
                ftarget=0.3,
                verbose=0
            ),
            refit_best_model=True,
            best_model_fit_kwargs=dict(
                save_built_model=False,
            ),
            save_to_json=False,
            max_threads=3
        )

    def notify_order(self, order):
        if order.status == order.Completed:
            self.log('-- Buy Exec @ {}'.format(order.executed.price))

    def _set_x(self):
        self.x = [
            AssetMADiff(self.data.close,
                        period=10,
                        csv=self.p.csv,
                        plotname='Close_diff_SMA_Close_10'),

            AssetMALogROC(self.data.close,
                          period=20,
                          movav=bt.indicators.MovAv.EMA,
                          csv=self.p.csv,
                          plotname='Close_diff_SMA_Close_20'),

            MAsDiff(self.data.close,
                    fast_period=9,
                    fast_movav=bt.indicators.MovAv.EMA,
                    slow_period=20,
                    slow_movav=bt.indicators.MovAv.EMA,
                    csv=self.p.csv,
                    plotname='EMA_Close_9_diff_EMA_Close_20'),

            MALogReturn(self.data.volume,
                        period=5,
                        movav_period=15,
                        movav=bt.indicators.MovAv.EMA,
                        csv=self.p.csv,
                        plotname='EMA_Volume_15_log_ret_5'),

            # coint
            CointLogRets(self.data.close,
                         self.data.close,
                         period0=1,
                         period1=15,
                         period=30,
                         csv=self.p.csv)

            # correl
            # obv
        ]

        for i, feat in enumerate(self.x):
            setattr(self, 'x{}'.format(i), feat)

    def _get_x(self) -> np.ndarray:
        _x = [x.get(0, len(self)) for x in self.x]
        return np.column_stack(_x)
