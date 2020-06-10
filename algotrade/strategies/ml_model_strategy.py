import backtrader as bt
import datetime as dt


class MLModelStrategy(bt.Strategy):
    params = dict(
        model_search_space=None,
        stop_loss=0.2,  # price is 2% less than the entry point
        trail=False,
        printout=False,
        csv=False,
    )

    def __init__(self):
        self.order = None
        self._model = None

        # Set timer to refit model every last trading of week
        self.add_timer(
            when=bt.timer.SESSION_END,
            weekdays=[5],
            weekcarry=True,
        )

    def log(self, txt, dt=None):
        if self.p.printout:
            dt = dt or self.data.datetime[0]
            if isinstance(dt, float):
                dt = bt.num2date(dt)
            print('[{}] {}'.format(dt.strftime("%Y-%m-%d %H:%M"), txt))

    def next(self):
        _, isowk, isowkday = self.datetime.date().isocalendar()
        txt = '-- next {}, {}, Week {}, Day {}, O {:.2f}, H {:.2f}, L {:.2f}, C {:.2f} - {}'.format(
            len(self),
            self.datetime.datetime(),
            isowk,
            isowkday,
            self.data.open[0],
            self.data.high[0],
            self.data.low[0],
            self.data.close[0],
            self.data.close.get(size=10))

        self.log(txt)

    def notify_timer(self, timer, when, *args, **kwargs):
        self.log('-- notify_timer {}, {} - O {:.2f}, H {:.2f}, L {:.2f}, C {:.2f} - {}'.format(
            when,
            len(self),
            self.data.open[0],
            self.data.high[0],
            self.data.low[0],
            self.data.close[0],
            self.data.close.get(size=10)))

        if self.order is None:
            self.log('-- Create buy order')
            self.order = self.buy()

    def notify_order(self, order):
        if order.status == order.Completed:
            self.log('-- Buy Exec @ {}'.format(order.executed.price))
