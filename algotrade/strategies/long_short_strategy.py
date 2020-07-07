import backtrader as bt
import backtrader.indicators as btind


class LongShortStrategy(bt.Strategy):
    """
    This strategy buys/sells upon the fast sma of the close price crossing upwards/downwards a
    slow sma of the close price.
    It can be a long-only strategy by setting the param "onlylong" to True
    """

    params = dict(
        use_ema=True,
        fast_period=9,
        slow_period=15,
        stop_loss=0.2,  # price is 2% less than the entry point
        trail=False,
        onlylong=False,
        printout=False,
        csv=False,
    )

    def log(self, txt, dt=None):
        if self.p.printout:
            dt = dt or self.data.datetime[0]
            if isinstance(dt, float):
                dt = bt.num2date(dt)
            print('[{}] {}'.format(dt.strftime("%Y-%m-%d %H:%M"), txt))

    def __init__(self):
        if self.p.use_ema:
            self.fast_ma = btind.MovAv.EMA(self.data.close, period=self.p.fast_period)
            self.slow_ma = btind.MovAv.EMA(self.data.close, period=self.p.slow_period)
        else:
            self.fast_ma = btind.MovAv.SMA(self.data.close, period=self.p.fast_period)
            self.slow_ma = btind.MovAv.SMA(self.data.close, period=self.p.slow_period)

        self.signal = btind.CrossOver(self.fast_ma, self.slow_ma)

        self.fast_ma.csv = self.p.csv
        self.slow_ma.csv = self.p.csv
        self.signal.csv = self.p.csv

    def start(self):
        self.log('Backtesting is about to start')

    def stop(self):
        self.log('Backtesting is finished')

    def next(self):
        if self.signal > 0.0:  # cross upwards
            if self.position:
                self.log('CLOSE SHORT @ %.2f' % self.data.close[0])
                self.close()

            self.log('BUY @ %.2f' % self.data.close[0])
            buy_order = self.buy(transmit=False)

            if not self.p.trail:
                stop_price = self.data.close[0] * (1.0 - self.p.stop_loss)
                self.log('SELL STOP @ %.2f' % stop_price)
                self.sell(
                    exectype=bt.Order.Stop,
                    price=stop_price,
                    parent=buy_order
                )
            else:
                self.log('SELL STOP TRAIL @ %.3f' % self.p.stop_loss)
                self.sell(
                    exectype=bt.Order.StopTrail,
                    trailpercent=self.p.stop_loss,
                    parent=buy_order
                )

        elif self.signal < 0.0:  # cross downwards
            if self.position:
                self.log('CLOSE LONG @ %.2f' % self.data.close[0])
                self.close()

            if not self.p.onlylong:
                self.log('SELL @ %.2f' % self.data.close[0])
                sell_order = self.sell(transmit=False)

                if not self.p.trail:
                    stop_price = self.data.close[0] * (1.0 + self.p.stop_loss)
                    self.log('BUY STOP @ %.2f' % stop_price)
                    self.buy(
                        exectype=bt.Order.Stop,
                        price=stop_price,
                        parent=sell_order
                    )
                else:
                    self.log('BUY STOP TRAIL @ %.3f' % self.p.stop_loss)
                    self.buy(
                        exectype=bt.Order.StopTrail,
                        trailpercent=self.p.stop_loss,
                        parent=sell_order
                    )

    def notify_order(self, order):
        if order.status in [bt.Order.Submitted, bt.Order.Accepted]:
            return  # Await further notifications

        if order.status == order.Completed:
            if order.isbuy():
                buytxt = 'BUY COMPLETE @ %.2f' % order.executed.price
                self.log(buytxt, order.executed.dt)
            else:
                selltxt = 'SELL COMPLETE @ %.2f' % order.executed.price
                self.log(selltxt, order.executed.dt)

        elif order.status in [order.Expired, order.Canceled, order.Margin]:
            self.log('%s' % order.Status[order.status])
            pass  # Simply log

    def notify_trade(self, trade):
        if trade.isclosed:
            self.log('TRADE PROFIT, GROSS %.2f, NET %.2f' % (trade.pnl, trade.pnlcomm))

        elif trade.justopened:
            self.log('TRADE OPENED, SIZE %2d' % trade.size)
