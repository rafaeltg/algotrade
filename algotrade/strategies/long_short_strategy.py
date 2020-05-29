import backtrader as bt
import backtrader.indicators as btind


class LongShortStrategy(bt.Strategy):
    """
    This strategy buys/sells upong the close price crossing
    upwards/downwards a Simple Moving Average.
    It can be a long-only strategy by setting the param "onlylong" to True
    """

    params = dict(
        fast_period=9,
        slow_period=15,
        stop_loss=0.2,  # price is 2% less than the entry point
        trail=False,
        printout=False,
        onlylong=False,
        csvcross=False,
    )

    def log(self, txt, dt=None):
        if self.p.printout:
            dt = dt or self.data.datetime[0]
            dt = bt.num2date(dt)
            print('%s, %s' % (dt.strftime("%Y-%m-%d %H:%M"), txt))

    def __init__(self):
        # To control operation entries
        self.orderid = None

        # Create SMAs
        fast_sma = btind.MovAv.SMA(self.data, period=self.p.fast_period)
        slow_sma = btind.MovAv.SMA(self.data, period=self.p.slow_period)

        # Create a CrossOver Signal from close an moving average
        self.signal = btind.CrossOver(fast_sma, slow_sma)
        self.signal.csv = self.p.csvcross

    def start(self):
        self.log('Backtesting is about to start')

    def stop(self):
        self.log('Backtesting is finished')

    def next(self):
        if self.orderid:
            return  # if an order is active, no new orders are allowed

        if self.signal > 0.0:  # cross upwards
            if self.position:
                self.log('CLOSE SHORT, %.2f' % self.data.close[0])
                self.close()

            self.log('BUY CREATE, %.2f' % self.data.close[0])
            buy_order = self.buy(transmit=False)

            if not self.p.trail:
                stop_price = self.data.close[0] * (1.0 - self.p.stop_loss)
                self.sell(
                    exectype=bt.Order.Stop,
                    price=stop_price,
                    parent=buy_order
                )
            else:
                self.sell(
                    exectype=bt.Order.StopTrail,
                    trailpercent=self.p.stop_loss,
                    parent=buy_order
                )

        elif self.signal < 0.0:  # cross downwards
            if self.position:
                self.log('CLOSE LONG, %.2f' % self.data.close[0])
                self.close()

            if not self.p.onlylong:
                self.log('SELL CREATE, %.2f' % self.data.close[0])
                sell_order = self.sell(transmit=False)

                if not self.p.trail:
                    stop_price = self.data.close[0] * (1.0 + self.p.stop_loss)
                    self.buy(
                        exectype=bt.Order.Stop,
                        price=stop_price,
                        parent=sell_order
                    )
                else:
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
                buytxt = 'BUY COMPLETE, %.2f' % order.executed.price
                self.log(buytxt, order.executed.dt)
            else:
                selltxt = 'SELL COMPLETE, %.2f' % order.executed.price
                self.log(selltxt, order.executed.dt)

        elif order.status in [order.Expired, order.Canceled, order.Margin]:
            self.log('%s,' % order.Status[order.status])
            pass  # Simply log

        # Allow new orders
        self.orderid = None

    def notify_trade(self, trade):
        if trade.isclosed:
            self.log('TRADE PROFIT, GROSS %.2f, NET %.2f' % (trade.pnl, trade.pnlcomm))

        elif trade.justopened:
            self.log('TRADE OPENED, SIZE %2d' % trade.size)
