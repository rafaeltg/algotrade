import backtrader as bt
import backtrader.indicators as btind


class LongShortStrategy(bt.Strategy):
    """
    This strategy buys/sells upong the close price crossing
    upwards/downwards a Simple Moving Average.
    It can be a long-only strategy by setting the param "onlylong" to True
    """

    params = dict(
        period=20,
        stake=1,
        printout=False,
        onlylong=False,
        csvcross=False,
    )

    def log(self, txt, dt=None):
        if self.p.printout:
            dt = dt or self.data.datetime[0]
            dt = bt.num2date(dt)
            print('%s, %s' % (dt.isoformat(), txt))

    def __init__(self):
        # To control operation entries
        self.orderid = None

        # Create SMA on 2nd data
        sma = btind.MovAv.SMA(self.data, period=self.p.period)
        # Create a CrossOver Signal from close an moving average
        self.signal = btind.CrossOver(self.data.close, sma)
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
                self.log('CLOSE SHORT , %.2f' % self.data.close[0])
                self.close()

            self.log('BUY CREATE , %.2f' % self.data.close[0])
            self.buy(size=self.p.stake)

        elif self.signal < 0.0:
            if self.position:
                self.log('CLOSE LONG , %.2f' % self.data.close[0])
                self.close()

            if not self.p.onlylong:
                self.log('SELL CREATE , %.2f' % self.data.close[0])
                self.sell(size=self.p.stake)

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
            self.log('%s ,' % order.Status[order.status])
            pass  # Simply log

        # Allow new orders
        self.orderid = None

    def notify_trade(self, trade):
        if trade.isclosed:
            self.log('TRADE PROFIT, GROSS %.2f, NET %.2f' % (trade.pnl, trade.pnlcomm))

        elif trade.justopened:
            self.log('TRADE OPENED, SIZE %2d' % trade.size)
