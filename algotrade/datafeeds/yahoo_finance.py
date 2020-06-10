import backtrader as bt
from .utils import _parse_dates


class YahooFinanceCSVData(bt.feeds.YahooFinanceCSVData):

    @classmethod
    def from_config(cls, **config):
        return cls(**_parse_dates(config))


class YahooFinanceData(bt.feeds.YahooFinanceData):

    @classmethod
    def from_config(cls, **config):
        return cls(**_parse_dates(config))
