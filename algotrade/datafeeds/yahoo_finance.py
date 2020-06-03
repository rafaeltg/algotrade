import backtrader as bt
from dateutil.parser import parse


class YahooFinanceCSVData(bt.feeds.YahooFinanceCSVData):

    @classmethod
    def from_config(cls, **config):
        fromdate = config.pop('fromdate', None)
        if fromdate is not None:
            fromdate = parse(fromdate)

        todate = config.pop('todate', None)
        if todate is not None:
            todate = parse(todate)

        return cls(fromdate=fromdate, todate=todate, **config)


class YahooFinanceData(bt.feeds.YahooFinanceData):

    def to_config(self) -> dict:
        config = self.params._getitems()
        config['fromdate'] = self.params.fromdate.strftime('%Y-%m-%d')
        config['enddate'] = self.params.todate.strftime('%Y-%m-%d')
        return config

    @classmethod
    def from_config(cls, **config):
        fromdate = config.pop('fromdate', None)
        if fromdate is not None:
            fromdate = parse(fromdate)

        todate = config.pop('todate', None)
        if todate is not None:
            todate = parse(todate)

        return cls(fromdate=fromdate, todate=todate, **config)
