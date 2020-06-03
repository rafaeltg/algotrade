import backtrader as bt


class MLModelStrategy(bt.Strategy):
    params = dict(
        model_search_space=None,
        stop_loss=0.2,  # price is 2% less than the entry point
        trail=False,
        printout=False,
        csv=False,
    )

    def __init__(self):
        # To control operation entries
        self.orderid = None

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
        pass

    def notify_timer(self, timer, when, *args, **kwargs):
        pass
